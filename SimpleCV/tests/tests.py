#!/usr/bin/python
# *To run this test you need python nose tools installed
# Run test just use:
#   nosetest tests.py

import os, sys
from SimpleCV import * 
from nose.tools import with_setup

#colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)


#images
testimage = "../sampleimages/9dots4lines.png"
testimage2 = "../sampleimages/aerospace.jpg"
whiteimage = "../sampleimages/white.png"
blackimage = "../sampleimages/black.png"
testimageclr = "../sampleimages/statue_liberty.jpg"
testbarcode = "../sampleimages/barcode.png"
testoutput = "../sampleimages/9d4l.jpg"


def setup_context():
  img = Image(testimage)
  
def destroy_context():
  img = ""

@with_setup(setup_context, destroy_context)
def test_loadsave():
  img = Image(testimage)
  img.save(testoutput)  
  if (os.path.isfile(testoutput)):
    os.remove(testoutput)
    pass
  else: 
    assert False
  
def test_bitmap():
  img = Image(testimage)
  bmp = img.getBitmap();
  if bmp.width > 0:
    pass
  else:
    assert False

#TODO: get this test working
#def test_matrix():
#  img = Image(testimage)
#  m = img.getMatrix()
#  if (m.rows == img.getBitmap().width):
#    pass
#  assert False
  
def test_scale():
  img = Image(testimage)
  thumb = img.scale(30,30)
  thumb.save(testoutput)

def test_copy():
  img = Image(testimage2)
  copy = img.copy()

  if (img[1,1] != copy[1,1] or img.size() != copy.size()):
    assert False 
  pass
  

def test_getitem():
  img = Image(testimage)
  colors = img[1,1]
  if (colors[0] == 255 and colors[1] == 255 and colors[2] == 255):
    pass
  else: 
    assert False

def test_getslice():
  img = Image(testimage)
  section = img[1:10,1:10]
  section.save(testoutput)
  pass


def test_setitem():
  img = Image(testimage)
  img[1,1] = (0, 0, 0)
  newimg = Image(img.getBitmap())
  colors = newimg[1,1]
  if (colors[0] == 0 and colors[1] == 0 and colors[2] == 0):
    pass
  else:
    assert False

def test_setslice():
  img = Image(testimage)
  img[1:10,1:10] = (0,0,0) #make a black box
  newimg = Image(img.getBitmap())
  section = newimg[1:10,1:10]
  for i in range(5):
    colors = section[i,0]
    if (colors[0] != 0 or colors[1] != 0 or colors[2] != 0):
      assert False  
  pass

def test_findCorners():
  img = Image(testimage2)
  corners = img.findCorners(25)
  if (len(corners) == 0):
    assert False 
  corners.draw()
  img.save(testoutput)
  
def test_meancolor():
  img = Image(testimage2)
  roi = img[1:50,1:50]
  
  r, g, b = roi.meanColor()

  if (r >= 0 and r <= 255 and g >= 0 and g <= 255 and b >= 0 and b <= 255):
    pass 

def test_smooth():
  img = Image(testimage2)
  img.smooth()
  img.smooth('bilateral', (3,3), 4, 1)
  img.smooth('blur', (3, 3))
  img.smooth('median', (3, 3))
  img.smooth('gaussian', (5,5), 0) 
  pass

def test_binarize():
  img =  Image(testimage2)
  binary = img.binarize()
  binary2 = img.binarize((60, 100, 200))
  hist = binary.histogram(20)
  hist2 = binary2.histogram(20)
  if (hist[0] + hist[-1] == np.sum(hist) and hist2[0] + hist2[-1] == np.sum(hist2)):
    pass
  else:
    assert False

def test_invert():
  img = Image(testimage2)
  clr = img[1,1]
  img = img.invert()

  if (clr[0] == (255 - img[1,1][0])):
    pass
  else:
    assert False


def test_size():
  img = Image(testimage2)
  (width, height) = img.size()
  if type(width) == int and type(height) == int and width > 0 and height > 0:
    pass
  else:
    assert False

def test_drawing():
  img = Image(testimageclr)
  img.drawCircle((5, 5), 3)
  img.drawLine((5, 5), (5, 8))
  
def test_splitchannels():  
  img = Image(testimageclr)
  (r, g, b) = img.splitChannels(True)
  (red, green, blue) = img.splitChannels()
  pass

def test_histogram():
  img = Image(testimage2)
  h = img.histogram(25)

  for i in h:
    if type(i) != int:
      assert False

  pass

def test_lines():
  img = Image(testimage2)
  lines = img.findLines()

  lines.draw()
  img.save(testoutput)

def test_feature_measures():
  img = Image(testimage2)
  
  fs = FeatureSet()
  fs.append(Corner(img, 5, 5))
  fs.append(Line(img, ((2, 2), (3,3))))

  if BLOBS_ENABLED:
    fs.append(img.findBlobs()[0])

  if ZXING_ENABLED:
    fake_barcode = Barcode(img, zxing.BarCode("""
file:default.png (format: FAKE_DATA, type: TEXT):
Raw result:
foo-bar|the bar of foo
Parsed result:
foo-bar 
the bar of foo
Also, there were 4 result points:
  Point 0: (24.0,18.0)
  Point 1: (21.0,196.0)
  Point 2: (201.0,198.0)
  Point 3: (205.23952,21.0)
"""))
    fs.append(fake_barcode) 

  for f in fs:
    a = f.area()
    l = f.length()
    c = f.meanColor()
    d = f.colorDistance()
    th = f.angle()
    pts = f.coordinates()
    dist = f.distanceFrom() #distance from center of image 

  fs1 = fs.sortDistance()
  fs2 = fs.sortAngle()
  fs3 = fs.sortLength()
  fs4 = fs.sortColorDistance()
  fs5 = fs.sortArea()
  

def test_blobs():
  if not BLOBS_ENABLED:
    return None 
  img = Image(testbarcode)
  blobs = img.findBlobs()

  blobs[0].draw((0, 255, 0))
  img.save(testoutput)  

  pass




def test_barcode():
  if not ZXING_ENABLED:
    return None

  nocode = Image(testimage).findBarcode()
  if nocode: #we should find no barcode in our test image 
    assert False
  code = Image(testbarcode).findBarcode() 
  
  if code.points:
    pass
    
def test_x():
  tmpX = Image(testimage).findLines().x()[0]

  if (tmpX > 0 and Image(testimage).size()[0]):
    pass
  else:
    assert False

def test_y():
  tmpY = Image(testimage).findLines().y()[0]

  if (tmpY > 0 and Image(testimage).size()[0]):
    pass
  else:
    assert False

def test_area():
  area_val = Image(testimage).findBlobs().area()[0]
  
  if(area_val > 0):
    pass
  else:
    assert False

def test_angle():
  angle_val = Image(testimage).findLines().angle()[0]

def test_image():
  img = Image(testimage)
  if(isinstance(img, Image)):
    pass
  else:
    assert False

def test_colordistance():
  img = Image(blackimage)
  (r,g,b) = img.splitChannels()
  avg = img.meanColor()
  
  c1 = Corner(img, 1, 1)
  c2 = Corner(img, 1, 2)
  if (c1.colorDistance(c2.meanColor()) != 0):
    assert False
  
  if (c1.colorDistance((0,0,0)) != 0):
    assert False

  if (c1.colorDistance((0,0,255)) != 255):
    assert False

  if (c1.colorDistance((255,255,255)) != sqrt(255**2 * 3)):
    assert False
    
  pass
  
def test_length():
  img = Image(testimage)
  val = img.findLines().length()

  if (val == None):
    assert False
  if (not isinstance(val, np.ndarray)):
    assert False
  if (len(val) < 0):
    assert False

  pass


  
  
def test_sortangle():
  img = Image(testimage)
  val = img.findLines().sortAngle()

  if(val[0].x < val[1].x):
    pass
  else:
    assert False
    
def test_sortarea():
  img = Image(testimage)
  val = img.findBlobs().sortArea()
  #FIXME: Find blobs may appear to be broken. Returning type none

def test_sortLength():
  img = Image(testimage)
  val = img.findLines().sortLength()
  #FIXME: Length is being returned as euclidean type, believe we need a universal type, either Int or scvINT or something.
 
#def test_distanceFrom():
#def test_sortColorDistance():
#def test_sortDistance():

def test_image_add():
  imgA = Image(testimage)
  imgB = Image(testimage2)

  imgC = imgA + imgB


  
  

  
#def test_image_subtract():
#def test_image_negative():
#def test_image_multiple():
#def test_image_divide():
#def test_image_and():
#def test_image_or():
#def test_image_edgemap():
#def test_image_filter():