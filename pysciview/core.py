import imagej

global GLVector

class PySciView(dict):
    ij = None

    # Config could be read from file
    def config(self):
        self['fiji_directory'] = './Fiji.app'
        return self

    def run(self,cmd='sc.iview.commands.LaunchViewer',args={}):
        if( args=={} ):
            return self.ij.command().run(cmd, True).get()
        else:
            #print(list(args.keys())[0] + '\t' + str(args[list(args.keys())[0]]))
            return self.ij.command().run(cmd, True, list(args.keys())[0], str(args[list(args.keys())[0]])).get()

    def create(self):
        self.ij = imagej.init(self['fiji_directory'],headless=False)
        import jnius
        global GLVector
        GLVector = jnius.autoclass('cleargl.GLVector')
        self.ij.ui().showUI()
        return self.run().getOutput('sciView')

