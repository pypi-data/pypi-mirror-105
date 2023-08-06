from PIL import Image
import numpy as np
import tqdm
from io import BytesIO




#test_change

class mplib_gif_wrapper():
    """
    Example
    -------
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax=mplib_gif_wrapper(ax,"test_wrapper.gif")


    #optional ax.reset_gif()
    for i in range(100):
        x=np.random.random((50))
        y=x**(i*0.02)
        x=np.random.random((100,100,3))
        ax.set_ylim(0,1)
        ax.set_xlim(0,1)
        ax.scatter(x,y)
    ---->gif saved as test_wrapper.gif

    Inputs:

    save_every: if None, save is only done explicitly withax.save()

    frames_per_second number of frames to display in one second of animation

    """
    def __init__(self,axes,fp,clear=True, save_every=10, frames_per_second = 5):

        self.fp=fp
        self.axes=axes
        self._clear=clear
        self.save_every=save_every
        self.counter=0
        self.list_plots=["scatter","plot","imshow"]
        self.list_ims=[]
        self._frames_per_second = frames_per_second

    def __getattr__(self,item):

        attr=getattr(self.axes,item)

        if item in self.list_plots:
            self.counter+=1
            self.list_ims.append(mplib_fig_2_image(self.axes.get_figure(),out="PIL"))

            if not(self.save_every == None):
                if self.counter%self.save_every==0:
                    self.save( frames_per_second = self._frames_per_second)

            if self._clear:
                self.axes.clear()

        return attr

    def reset_gif(self, ):

        self.counter=0
        self.list_ims=[]

    def save(self, frames_per_second = 5, loop = 0):

        duration = 1000./frames_per_second  ##ms per frame
        make_gif(self.list_ims,self.fp, duration = duration, loop = loop)





def make_gif(ims_list,fp,optimize=False,duration=40,loop=0,**kwargs):
    """ims_list list of np array (w,h,c) or list of pil ims
    out filepath
    """
    if isinstance(ims_list[0],Image.Image):
        ims=ims_list
    elif isinstance(ims_list[0],np.ndarray):
        ims=[numpy_2_image(im,out="PIL") for im in ims_list]

    ims[0].save(fp,
               save_all=True, append_images=ims[1:],
                optimize=False, duration = duration, loop = loop,**kwargs)

def _pil_2_image(im_pil,out=None,format="JPEG"):
    if out=="bytes":
        buf=BytesIO()
        im_pil.save(buf,format=format)
        bytes_out=buf.seek(0)
        return bytes_out
    elif out=="PIL":
        return im_pil
    else:
        im_pil.save(out,format=format)



def mplib_fig_2_image(fig,out="PIL",format="JPEG"):
    """ matplotlib figure to image
            input: matplotlib figure
            out : BytesIO instance,file_path,"bytes"
        specify the output, if BytesIO instance, bytes will be writen in the instance
    """
    buf=BytesIO()
    fig.savefig(buf)
    im_pil=Image.open(buf)
    im_pil = im_pil.convert('RGB')
    return _pil_2_image(im_pil,out=out,format=format)


def numpy_2_image(np_array,out=None,format="JPEG"):
    """Np array (Width,Height,Channels)  to image bytes or pil
    Input
    -----
        np_array : (w,h,c) or filepath of .npy file
        out : BytesIO instance,file_path,"bytes"
        specify the output, if BytesIO instance, bytes will be writen in the instance
    """
    if isinstance(np_array,str):
        np_array=np.load(np_array)
    array=np_array.astype(np.uint8)
    im_pil=Image.fromarray(array)

    return _pil_2_image(im_pil,out=out,format=format)




def image_2_numpy(fp):
    """
    fp might be bytes, Buf, filepath, or PIL Jpeg image
    """
    if isinstance(fp,bytes):
        read=BytesIO(fp)
        read=Image.open(read)
    elif isinstance(fp,Image.Image):
        read=fp
    else:
        read=Image.open(fp)
    out=np.array(read)
    return out
