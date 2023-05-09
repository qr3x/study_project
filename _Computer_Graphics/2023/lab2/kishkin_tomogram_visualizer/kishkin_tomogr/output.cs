using kishkin_tomogr_input;

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;

using OpenTK;
using OpenTK.Graphics.OpenGL;
using System.Drawing.Imaging;

namespace kishkin_tomogr_output
{
    
    class View
    {
        Bitmap textureImage;
        int VBOtexture;

        public View() { }

        public void SetupView(int width, int height)
        {
            GL.ShadeModel(ShadingModel.Smooth);
            GL.MatrixMode(MatrixMode.Projection);
            GL.LoadIdentity();
            GL.Ortho(0, Bin.X, 0, Bin.Y, -1, 1);
            GL.Viewport(0, 0, width, height);
        }

        Color TransferFunction(short value, int minTF, int widthTF)
        {
            int min = minTF;
            int max = minTF + widthTF;
            int newVal = Clamp((value - min) * 255 / (max - min), 0, 255);
            return Color.FromArgb(255, newVal, newVal, newVal);
        }

        public int Clamp(int value, int min = 0, int max = 255)
        {
            if (value < min)
                return min;
            if (value > max)
                return max;
            return value;
        }

        public void DrawQuards(int layerNumber, int minTF, int widthTF, bool isQuads)
        {
            GL.Clear(ClearBufferMask.ColorBufferBit | ClearBufferMask.DepthBufferBit);
            if (isQuads)
            {
                GL.Begin(BeginMode.Quads);
                for (int x_coord = 0; x_coord < Bin.X - 1; x_coord++)
                    for (int y_coord = 0; y_coord < Bin.Y - 1; y_coord++)
                    {
                        short value;

                        // 1ая вершина
                        value = Bin.array[x_coord + y_coord * Bin.X + layerNumber * Bin.X * Bin.Y];
                        GL.Color3(TransferFunction(value, minTF, widthTF));
                        GL.Vertex2(x_coord, y_coord);

                        // 2ая вершина
                        value = Bin.array[x_coord + (y_coord + 1) * Bin.X + layerNumber * Bin.X * Bin.Y];
                        GL.Color3(TransferFunction(value, minTF, widthTF));
                        GL.Vertex2(x_coord, y_coord + 1);

                        // 3ья вершина
                        value = Bin.array[x_coord + 1 + (y_coord + 1) * Bin.X + layerNumber * Bin.X * Bin.Y];
                        GL.Color3(TransferFunction(value, minTF, widthTF));
                        GL.Vertex2(x_coord + 1, y_coord + 1);

                        // 4ая вершина
                        value = Bin.array[x_coord + 1 + y_coord * Bin.X + layerNumber * Bin.X * Bin.Y];
                        GL.Color3(TransferFunction(value, minTF, widthTF));
                        GL.Vertex2(x_coord + 1, y_coord);
                    }
            }
            else
            {
                for (int y_coord = 0; y_coord < Bin.Y - 1; y_coord++)
                {
                    GL.Begin(BeginMode.QuadStrip);
                    short value;
                    value = Bin.array[0 + y_coord * Bin.X + layerNumber * Bin.X * Bin.Y];
                    GL.Color3(TransferFunction(value, minTF, widthTF));
                    GL.Vertex2(0, y_coord);

                    value = Bin.array[0 + (y_coord + 1) * Bin.X + layerNumber * Bin.X * Bin.Y];
                    GL.Color3(TransferFunction(value, minTF, widthTF));
                    GL.Vertex2(0, y_coord + 1);
                    for (int x_coord = 0; x_coord < Bin.X - 1; x_coord++)
                    {
                        value = Bin.array[x_coord + 1 + y_coord * Bin.X + layerNumber * Bin.X * Bin.Y];
                        GL.Color3(TransferFunction(value, minTF, widthTF));
                        GL.Vertex2(x_coord + 1, y_coord);

                        value = Bin.array[x_coord + 1 + (y_coord + 1) * Bin.X + layerNumber * Bin.X * Bin.Y];
                        GL.Color3(TransferFunction(value, minTF, widthTF));
                        GL.Vertex2(x_coord + 1, y_coord + 1);
                    }
                    GL.End();
                }
                /*GL.Begin(BeginMode.QuadStrip);
                for (int x_coord = 0; x_coord < Bin.X - 1; x_coord++)
                {
                    Color color0, color1;
                    short value;
                    // 1ая вершина
                    value = Bin.array[x_coord + layerNumber * Bin.X * Bin.Y];
                    color0 = TransferFunction(value, minTF, widthTF);

                    // 2ая вершина
                    value = Bin.array[x_coord + Bin.X + layerNumber * Bin.X * Bin.Y];
                    color1 = TransferFunction(value, minTF, widthTF);

                    for (int y_coord = 0; y_coord < Bin.Y - 1; y_coord++)
                    {
                        // 1ая вершина
                        GL.Color3(color0);
                        GL.Vertex2(x_coord, y_coord);

                        // 2ая вершина
                        GL.Color3(color1);
                        GL.Vertex2(x_coord, y_coord + 1);

                        // 3ья вершина
                        value = Bin.array[x_coord + 1 + (y_coord + 1) * Bin.X + layerNumber * Bin.X * Bin.Y];
                        color0 = TransferFunction(value, minTF, widthTF);
                        GL.Color3(color0);
                        GL.Vertex2(x_coord + 1, y_coord + 1);

                        // 4ая вершина
                        value = Bin.array[x_coord + 1 + y_coord * Bin.X + layerNumber * Bin.X * Bin.Y];
                        color1 = TransferFunction(value, minTF, widthTF);
                        GL.Color3(color1);
                        GL.Vertex2(x_coord + 1, y_coord);
                    }
                }*/
            }
            GL.End();
        }

        public void Load2DTexture()
        {
            GL.BindTexture(TextureTarget.Texture2D, VBOtexture);
            BitmapData data = textureImage.LockBits(
                new System.Drawing.Rectangle(0, 0, textureImage.Width, textureImage.Height),
                ImageLockMode.ReadOnly,
                System.Drawing.Imaging.PixelFormat.Format32bppArgb
            );
            GL.TexImage2D(
                TextureTarget.Texture2D,
                0,
                PixelInternalFormat.Rgba,
                data.Width,
                data.Height,
                0,
                OpenTK.Graphics.OpenGL.PixelFormat.Bgra,
                PixelType.UnsignedByte,
                data.Scan0
            );
            textureImage.UnlockBits(data);
            GL.TexParameter(TextureTarget.Texture2D, TextureParameterName.TextureMinFilter, (int)TextureMinFilter.Linear);
            GL.TexParameter(TextureTarget.Texture2D, TextureParameterName.TextureMinFilter, (int)TextureMinFilter.Linear);

            ErrorCode Er = GL.GetError();
            string str = Er.ToString();
        }

        public void generateTextureImage(int layerNumber, int minTF, int widthTF)
        {
            textureImage = new Bitmap(Bin.X, Bin.Y);
            for (int i = 0; i < Bin.X; ++i)
                for (int j = 0; j < Bin.Y; ++j)
                {
                    int pixelNumber = i + j * Bin.X + layerNumber * Bin.X * Bin.Y;
                    textureImage.SetPixel(i, j, TransferFunction(Bin.array[pixelNumber], minTF, widthTF));
                }
        }

        public void drawTexture()
        {
            GL.Clear(ClearBufferMask.ColorBufferBit | ClearBufferMask.DepthBufferBit);
            GL.Enable(EnableCap.Texture2D);
            GL.BindTexture(TextureTarget.Texture2D, VBOtexture);

            GL.Begin(BeginMode.Quads);
            GL.Color3(Color.White);

            GL.TexCoord2(0f, 0f);
            GL.Vertex2(0, 0);

            GL.TexCoord2(0f, 1f);
            GL.Vertex2(0, Bin.Y);

            GL.TexCoord2(1f, 1f);
            GL.Vertex2(Bin.X, Bin.Y);

            GL.TexCoord2(1f, 0f);
            GL.Vertex2(Bin.X, 0);

            GL.End();

            GL.Disable(EnableCap.Texture2D);
        }
    }
}
