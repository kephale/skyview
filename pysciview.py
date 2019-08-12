import imagej

config = {'fiji_directory':'./Fiji.app'}

ij = imagej.init(config['fiji_directory'],headless=False)
ij.ui().showUI()
