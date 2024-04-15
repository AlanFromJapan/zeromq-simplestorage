from PIL import Image

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
        