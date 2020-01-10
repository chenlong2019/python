from pygeotools.lib import iolib, warplib, malib
fn1 = 'D:\\shapedata\\result\\2016-spectral16d366ae8.tif'
fn2 = 'D:\\shapedata\\result\\2016-spectral16d366ae8.tif'
ds_list = warplib.memwarp_multi_fn([fn1, fn2], res='max', extent='intersection', t_srs='first', r='cubic')
r1 = iolib.ds_getma(ds_list[0])
r2 = iolib.ds_getma(ds_list[1])
rdiff = r1 - r2
malib.print_stats(rdiff)
out_fn = 'D:\\shapedata\\result\\2016-3456564344343434.tif'
iolib.writeGTiff(rdiff, out_fn, ds_list[0])