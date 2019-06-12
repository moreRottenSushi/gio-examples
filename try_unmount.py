"""
Good reads: https://www.micahcarrick.com/asynchronous-read-in-python-with-gio.html
            https://sjohannes.wordpress.com/2009/11/30/gio-tutorial-stream-io/

For Error Messages: http://webreflection.github.io/gjs-documentation/Gio-2.0/Gio.IOErrorEnum.html
If "Gio.File.mount_enclosing_volume" doesn't work try "Gio.File.mount_mountable", try if you need the -m parameter in the terminal commandline with gio mount -m "ftp://domain.de/test/test".
"""

from gi.repository import Gio, GLib

class GioMount():

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def cancel(self):
        # This could be connected to the "clicked" signal of a Gtk.Button
        print ("Canceling asynchronous operation...")
        self._cancellable.cancel()

    # Mount stuff like: uri = "ftp://websitename.de/directory/directory/"
    def try_mount(self, uri):
        print("Mounting: %s" % uri)

        fileg = Gio.File.new_for_uri(uri)
        self._cancellable.reset()
        fileg.mount_enclosing_volume(Gio.MountMountFlags(0), None, self._cancellable, self._mount_finished, user_data= None)

    #Callback when mounting is finished. Basically print the error message, when it went wrong.
    def _mount_finished(self, fileg, result, user_data = None):

        try:
            filemount = fileg.mount_enclosing_volume_finish(result)
            print("\nFile mount successful: " + str(filemount))
        except GLib.GError as error:
            print("Mount finished callback")
            if error.code == Gio.IOErrorEnum.CANCELLED:
                print("Alright then, we've aborted the read operation.")
            elif error.code == Gio.IOErrorEnum.ALREADY_MOUNTED:
                print("I guess its already mounted (Gio.IOErrorEnum.ALREADY_MOUNTED.")
            else:
                print( str(error))

        #print("\tQuit main loop after this.")
        loop.quit()

    # Unmounting something.
    def try_unmount(self, uri):
        print("Unmountable? %s" % uri)

        fileg = Gio.File.new_for_uri(uri)
        #print(fileg.get_uri())
        #fileg.unmount_mountable(Gio.MountUnmountFlags(1), self._cancellable, self._unmount_finished, user_data=None)  #Do a MountUnmountFlags(0) if not forcing unmount.



        try:
            gm = fileg.find_enclosing_mount(self._cancellable)  # There would be an async variant as well.
            #print("\nFilemount: \n")
            #print(gm)
            gm.unmount(Gio.MountUnmountFlags(1),self._cancellable,self._unmount_finished, None)


        except GLib.GError as error:
            if error.code == Gio.IOErrorEnum.CANCELLED:
                print("Alright then, we've aborted the read operation.")
            if error.code == Gio.IOErrorEnum.NOT_FOUND:
                print("Didn't find the file mount to unmount.")
            else:
                print(str(error))


    # Callback when unmounting is finished. Basically print the error message, when it went wrong.
    def _unmount_finished(self, fileg, result, user_data=None):
        try:
            filemount = fileg.unmount_finish(result)
            print("File unmount successful: " + str(filemount))

        except GLib.GError as error:
            print("Mount finished callback")
            if error.code == Gio.IOErrorEnum.CANCELLED:
                print("Alright then, we've aborted the read operation.")

            else:

                print(str(error))

        #print("\tQuit main loop after this.")
        loop.quit()


if __name__ == "__main__":

    remotepath = '/public_html/dir/dir/dir/dir/'
    domain = 'ftp://domain.de'

    gfo = GioMount()
    gfo.try_mount(domain + remotepath)  #to mount something
    gfo.try_unmount(domain+remotepath)    # to unmount something (read other comments)


    #print ("\tEntering GLib main loop")
    loop = GLib.MainLoop()
    loop.run()

