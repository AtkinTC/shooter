from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

class GL_Texture:
#32 bit image with alpha channel
    def __init__(self, filename):
        self.tex_ID=0
        self.width=0
        self.height=0
        self.LoadTexture(filename)

    def LoadTexture(self,filename):
        try:
            tex_surface = pygame.image.load(filename)
            tex_data = pygame.image.tostring(tex_surface, 'RGBA', 1)

            self.width, self.height = tex_surface.get_size()

            self.tex_ID = glGenTextures(1)

            glBindTexture(GL_TEXTURE_2D, self.tex_ID)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height,
                            0, GL_RGBA, GL_UNSIGNED_BYTE, tex_data)
            glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        except:
            print "unable to open texture: %s"%(filename)

    def __del__(self):
        glDeleteTextures(self.tex_ID)
