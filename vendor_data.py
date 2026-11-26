"""One-time archive import; Python 3 standard library only. No runtime downloads.
Run from any directory: python3 project/vendor_data.py
Writes data.js atomically only after every download and validation succeeds.
"""
import json
import math
from pathlib import Path
import re
import statistics
import struct
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
TARGETS = [('TrES-2 b','011446443'), ('HAT-P-7 b','010666592'),
           ('HAT-P-11 b','010748390'), ('Kepler-5 b','008190721'),
           ('Kepler-6 b','010857861'), ('Kepler-7 b','005780885'),
           ('Kepler-8 b','006922244'), ('Kepler-17 b','010619192')]

def fetch(url):
    print('Downloading', url, flush=True)
    with urllib.request.urlopen(url, timeout=90) as response:
        return response.read()

def fits_lightcurve(blob):
    """Read the TIME, PDCSAP_FLUX and SAP_QUALITY binary table columns."""
    offset = 0
    sizes = {'L':1,'X':1,'B':1,'I':2,'J':4,'K':8,'A':1,'E':4,'D':8,'C':8,'M':16,'P':8,'Q':16}
    while offset < len(blob):
        start = offset
        header = {}
        while True:
            card = blob[offset:offset+80].decode('ascii')
            offset += 80
            if card[:8].strip() == 'END':
                break
            if card[8:10] == '= ':
                header[card[:8].strip()] = card[10:].split('/')[0].strip().strip("'").strip()
        offset = start + math.ceil((offset-start)/2880)*2880
        axes = int(header.get('NAXIS',0))
        size = abs(int(header.get('BITPIX',8)))//8 if axes else 0
        for axis in range(1,axes+1):
            size *= int(header['NAXIS'+str(axis)])
        size += int(header.get('PCOUNT',0))
        if header.get('XTENSION') == 'BINTABLE':
            columns = {}
            pos = 0
            for i in range(1,int(header['TFIELDS'])+1):
                count, kind = re.fullmatch(r'(\d*)([A-Z])',header['TFORM'+str(i)]).groups()
                count = int(count or 1)
                columns[header['TTYPE'+str(i)]] = (pos,kind)
                pos += math.ceil(count/8) if kind=='X' else count*sizes[kind]
            if all(key in columns for key in ['TIME','PDCSAP_FLUX','SAP_QUALITY']):
                def value(row,key):
                    col,kind=columns[key]
                    return struct.unpack_from('>'+{'D':'d','E':'f','J':'i','K':'q','I':'h'}[kind],blob,row+col)[0]
                points=[]
                for row in range(int(header['NAXIS2'])):
                    base=offset+row*int(header['NAXIS1'])
                    t,f,q=[value(base,key) for key in ['TIME','PDCSAP_FLUX','SAP_QUALITY']]
                    if q==0 and math.isfinite(t) and math.isfinite(f) and f>0:
                        points.append([t,f])
                return points
        offset += math.ceil(size/2880)*2880
    raise ValueError('No valid Kepler flux table in downloaded FITS')

def main():
    targets=[]
    for name,kic in TARGETS:
        query="select pl_name,pl_orbper,pl_tranmid,pl_trandur,pl_trandep from ps where default_flag=1 and pl_name='"+name+"'"
        metadata_url='https://exoplanetarchive.ipac.caltech.edu/TAP/sync?'+urllib.parse.urlencode({'query':query,'format':'json'})
        rows=json.loads(fetch(metadata_url))
        if len(rows)!=1:
            raise ValueError('Expected one default archive solution for '+name)
        meta=rows[0]
        if any(meta[k] is None for k in ['pl_orbper','pl_tranmid','pl_trandur']):
            raise ValueError('Missing ephemeris for '+name)
        source=f'https://archive.stsci.edu/missions/kepler/lightcurves/{kic[:4]}/{kic}/kplr{kic}-2009166043257_llc.fits'
        points=fits_lightcurve(fetch(source))
        median=statistics.median(p[1] for p in points)
        # Q1 long cadence typically fits within the 1–5k budget without decimation.
        stride=max(1,math.ceil(len(points)/5000))
        points=[[round(t,7),round(f/median,8)] for t,f in points[::stride]]
        if len(points)<500:
            raise ValueError('Too few real observations for '+name)
        period=float(meta['pl_orbper'])
        epoch=float(meta['pl_tranmid'])-2454833
        epochs=[]
        n=math.ceil((points[0][0]-epoch)/period)
        while epoch+n*period<=points[-1][0]:
            epochs.append(round(epoch+n*period,7))
            n+=1
        targets.append(dict(name=name,kic=kic,category='Confirmed planet',period=period,
                            epoch=epoch,duration=float(meta['pl_trandur']),depth=meta['pl_trandep'],
                            epochs=epochs,points=points,source=source,metadataSource=metadata_url,
                            processing='Q1; SAP_QUALITY == 0; finite positive PDCSAP_FLUX / median; stride '+str(stride)))
    output=ROOT/'data.js.tmp'
    output.write_text('window.TRANSIT_DATA = '+json.dumps({'targets':targets},separators=(',',':'))+';\n')
    output.replace(ROOT/'data.js')
    print('Vendored',len(targets),'real targets. Binary and non-detection controls still require verified data.')

if __name__=='__main__':
    main()
