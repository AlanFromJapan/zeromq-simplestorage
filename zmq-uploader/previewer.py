from PIL import Image
import grbl2image.grbl2image as G2I

class PreviewerImage():
    def __init__(self) -> None:
        pass

    def capableExt(self):
        return ['jpg', 'jpeg', 'png', 'gif', 'bmp']
    
    def preview(self, file):
        try:
            img = Image.open(file)
            return img
        except Exception as e:
            print(e)
        

class PreviewerGRBL():
    def __init__(self) -> None:
        pass

    def capableExt(self):
        return ['gcode', 'nc', 'gc']
    
    def preview(self, file):
        try:
            #Generate the PIL Image object based on sample code
            img, _ = G2I.processFile(file, color="black")

            #final flip because the image 0,0 is top left and for us human it's at the bottom left
            img = img.transpose(Image.FLIP_TOP_BOTTOM)    
            print ("Image generated")
            return img
        except Exception as e:
            print(e)