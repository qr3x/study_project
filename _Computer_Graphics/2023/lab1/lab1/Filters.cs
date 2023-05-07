using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Drawing;
using System.ComponentModel;
using System.Security.Policy;

namespace Filters_Kishkin
{
    abstract class Filters
    {
        protected abstract Color calculateNewPixelColor(Bitmap sourceImage, int x, int y);

        public int Clamp(int value, int min = 0, int max = 255)
        {
            if (value < min)
                return min;
            if (value > max)
                return max;
            return value;
        }

        public int getIntensity(int R, int G, int B)
        {
             return (int)(0.299 * R + 0.587 * G + 0.114 * B);
        }

        public Color getMovedPixel(Bitmap sourceImage, int x, int y, int moveX, int moveY)
        {
            int width = sourceImage.Width;
            int height = sourceImage.Height;
            int newX = x + moveX;
            int newY = y + moveY;

            if (0 <= newX && newX < width && 0 <= newY && newY < height)
                return sourceImage.GetPixel(x + moveX, y + moveY);
            return Color.FromArgb(0, 0, 0);
        }

        public virtual Bitmap processImage(Bitmap sourceImage, BackgroundWorker worker)
        {
            if (sourceImage == null)
                return null;
            Bitmap resultImage = new Bitmap(sourceImage.Width, sourceImage.Height);

            for (int i = 0; i < sourceImage.Width; i++)
            {
                worker.ReportProgress((int)((float)i / resultImage.Width * 100));
                if (worker.CancellationPending)
                    return null;

                for (int j = 0; j < sourceImage.Height; j++)
                {
                    resultImage.SetPixel(i, j, calculateNewPixelColor(sourceImage, i, j));
                }
            }
            return resultImage;
        }
    }

    class InvertFilter : Filters
    {
        protected override Color calculateNewPixelColor(Bitmap sourceImage, int x, int y)
        {
            Color sourceColor = sourceImage.GetPixel(x, y);
            Color resultColor = Color.FromArgb(255 - sourceColor.R,
                                               255 - sourceColor.G,
                                               255 - sourceColor.B);
            return resultColor;
        }
    }

    class GrayScaleFilter : Filters
    {
        protected override Color calculateNewPixelColor(Bitmap sourceImage, int x, int y)
        {
            Color sourceColor = sourceImage.GetPixel(x, y);
            int intensity = getIntensity(sourceColor.R, sourceColor.G, sourceColor.B);
            Color resultColor = Color.FromArgb(Clamp(intensity), Clamp(intensity), Clamp(intensity));
            return resultColor;
        }
    }

    class HalfGrayScaleFilter : Filters
    {
        protected override Color calculateNewPixelColor(Bitmap sourceImage, int x, int y)
        {
            Color sourceColor = sourceImage.GetPixel(x, y);
            int intensity = getIntensity(sourceColor.R, sourceColor.G, sourceColor.B);
            Color resultColor = Color.FromArgb(Clamp(intensity), Clamp(intensity), Clamp(intensity));
            return resultColor;
        }

        public override Bitmap processImage(Bitmap sourceImage, BackgroundWorker worker)
        {
            if (sourceImage == null)
                return null;
            Bitmap resultImage = new Bitmap(sourceImage.Width, sourceImage.Height);
            double medianCoef = (double)sourceImage.Height / sourceImage.Width;

            for (int i = 0; i < sourceImage.Width; i++)
            {
                worker.ReportProgress((int)((float)i / resultImage.Width * 100));
                if (worker.CancellationPending)
                    return null;

                for (int j = 0; j < (int)(i * medianCoef); j++)
                {
                    resultImage.SetPixel(i, j, calculateNewPixelColor(sourceImage, i, j));
                }
                for (int j = (int)(i * medianCoef); j < resultImage.Height; j++)
                {
                    resultImage.SetPixel(i, j, sourceImage.GetPixel(i, j));
                }
            }
            return resultImage;
        }
    }

    class SepiaFilter : Filters
    {
        protected double k;

        public SepiaFilter(double k = 40)
        {
            this.k = k;
        }

        protected override Color calculateNewPixelColor(Bitmap sourceImage, int x, int y)
        {
            Color sourceColor = sourceImage.GetPixel(x, y);
            int intensity = getIntensity(sourceColor.R, sourceColor.G, sourceColor.B);
            int R = (int)(intensity + 2 * k);
            int G = (int)(intensity + 0.5 * k);
            int B = (int)(intensity - k);
            Color resultColor = Color.FromArgb(Clamp(R), Clamp(G), Clamp(B));
            return resultColor;
        }
    }

    class BrightnessFilter : Filters
    {
        protected override Color calculateNewPixelColor(Bitmap sourceImage, int x, int y)
        {
            int constant = 40;
            Color sourceColor = sourceImage.GetPixel(x, y);
            Color resultColor = Color.FromArgb(Clamp(sourceColor.R + constant), Clamp(sourceColor.G + constant), Clamp(sourceColor.B + constant));
            return resultColor;
        }
    }

    class MoveXtoRigthFilter: Filters
    {
        protected override Color calculateNewPixelColor(Bitmap sourceImage, int x, int y)
        {
            int constant = -50;
            return getMovedPixel(sourceImage, x, y, constant, 0);
        }
    }

    class GlassFilter : Filters
    {
        protected override Color calculateNewPixelColor(Bitmap sourceImage, int x, int y)
        {
            /*TODO: dont work*/
            Random random = new Random();
            Color sourceColor = sourceImage.GetPixel(x, y);
            int idX = x + 10 * (int)(random.Next(1) - 0.5);
            int idY = y + 10 * (int)(random.Next(1) - 0.5);
            Color resultColor = sourceImage.GetPixel(Clamp(idX, 0, sourceImage.Width - 1), Clamp(idY, 0, sourceImage.Height - 1));
            return resultColor;
        }
    }

    class LinearCorrection : Filters
    {
        protected override Color calculateNewPixelColor(Bitmap sourceImage, int x, int y)
        {
            return Color.FromArgb(0, 0, 0);
        }

        public override Bitmap processImage(Bitmap sourceImage, BackgroundWorker worker)
        {

            if (sourceImage == null)
                return null;
            Bitmap resultImage = new Bitmap(sourceImage.Width, sourceImage.Height);

            int Rmin = 255;
            int Rmax = 0;
            double R;

            int Gmin = 255;
            int Gmax = 0;
            double G;

            int Bmin = 255;
            int Bmax = 0;
            double B;

            Color color;
            for (int i = 0; i < sourceImage.Width; i++)
            {
                worker.ReportProgress((int)((float)i / resultImage.Width * 50));
                if (worker.CancellationPending)
                    return null;

                for (int j = 0; j < sourceImage.Height; j++)
                {
                    color = sourceImage.GetPixel(i, j);

                    if (color.R < Rmin)
                        Rmin = color.R;
                    if (color.R > Rmax)
                        Rmax = color.R;

                    if (color.G < Gmin)
                        Gmin = color.G;
                    if (color.G > Gmax)
                        Gmax = color.G;

                    if (color.B < Bmin)
                        Bmin = color.B;
                    if (color.B > Bmax)
                        Bmax = color.B;
                }
            }

            for (int i = 0; i < sourceImage.Width; i++)
            {
                worker.ReportProgress(50 + (int)((float)i / resultImage.Width * 50));
                if (worker.CancellationPending)
                    return null;

                for (int j = 0; j < sourceImage.Height; j++)
                {
                    color = sourceImage.GetPixel(i, j);


                    resultImage.SetPixel(i, j, Color.FromArgb((color.R - Rmin) * 255 / (Rmax - Rmin),
                                                              (color.G - Gmin) * 255 / (Gmax - Gmin),
                                                              (color.B - Bmin) * 255 / (Bmax - Bmin)));
                }
            }
            return resultImage;
        }
    }

    class MatrixFilter : Filters
    {
        protected float[,] kernel = null;

        protected MatrixFilter() { }

        public MatrixFilter(float[,] kernel)
        {
            this.kernel = kernel;
        }

        protected override Color calculateNewPixelColor(Bitmap sourceImage, int x, int y)
        {
            int radiusX = kernel.GetLength(0) / 2;
            int radiusY = kernel.GetLength(1) / 2;

            float resultR = 0, resultG = 0, resultB = 0;
            for (int l = -radiusY; l <= radiusY; l++)
                for (int k = -radiusX; k <= radiusX; k++)
                {
                    int idX = Clamp(x + k, 0, sourceImage.Width - 1);
                    int idY = Clamp(y + l, 0, sourceImage.Height - 1);
                    Color neighborColor = sourceImage.GetPixel(idX, idY);
                    resultR += neighborColor.R * kernel[k + radiusX, l + radiusY];
                    resultG += neighborColor.G * kernel[k + radiusX, l + radiusY];
                    resultB += neighborColor.B * kernel[k + radiusX, l + radiusY];
                }

            return Color.FromArgb(Clamp((int)resultR), Clamp((int)resultG), Clamp((int)resultB));
        }
    }

    class BlueFilter : MatrixFilter
    {
        public BlueFilter()
        {
            int sizeX = 3;
            int sizeY = 3;
            kernel = new float[sizeX, sizeY];
            for (int i = 0; i < sizeX; i++)
                for (int j = 0; j < sizeY; j++)
                    kernel[i, j] = 1.0f / (float)(sizeX * sizeY);
        }
    }

    class GaussianFilter : MatrixFilter
    {
        public GaussianFilter()
        {
            createGaussianKernel(3, 2);
        }

        public void createGaussianKernel(int radius, float sigma)
        {
            int size = 2 * radius + 1;
            kernel = new float[size, size];
            float norm = 0;
            for (int i = -radius; i <= radius; i++)
                for (int j = -radius; j <= radius; j++)
                {
                    kernel[i + radius, j + radius] = (float)(Math.Exp(-(i * i + j * j) / (2 * sigma * sigma)));
                    norm += kernel[i + radius, j + radius];
                }
            for (int i = 0; i < size; i++)
                for (int j = 0; j < size; j++)
                    kernel[i, j] /= norm;
        }
    }

    class SobelFilter : MatrixFilter
    {
        protected float[,] Gy = null;
        protected float[,] Gx = null;

        public SobelFilter()
        {
            Gy = new float[,] { { -1, -2, -1 },
                                { 0,   0,  0 },
                                { 1,   2,  1 } };

            Gx = new float[,] { { -1, 0, 1 },
                                { -2, 0, 2 },
                                { -1, 0, 1 } };
        }

        protected override Color calculateNewPixelColor(Bitmap sourceImage, int x, int y)
        {
            int radius = 1;

            float colorXR = 0, colorXG = 0, colorXB = 0;
            float colorYR = 0, colorYG = 0, colorYB = 0;
            int resultR, resultG, resultB;
            for (int l = -radius; l <= radius; l++)
                for (int k = -radius; k <= radius; k++)
                {
                    int idX = Clamp(x + k, 0, sourceImage.Width - 1);
                    int idY = Clamp(y + l, 0, sourceImage.Height - 1);
                    Color neighborColor = sourceImage.GetPixel(idX, idY);

                    colorXR += neighborColor.R * Gx[radius + k, radius + l];
                    colorXG += neighborColor.G * Gx[radius + k, radius + l];
                    colorXB += neighborColor.B * Gx[radius + k, radius + l];

                    colorYR += neighborColor.R * Gy[radius + k, radius + l];
                    colorYG += neighborColor.G * Gy[radius + k, radius + l];
                    colorYB += neighborColor.B * Gy[radius + k, radius + l];
                }
            resultR = getCountedColor(colorXR, colorYR);
            resultG = getCountedColor(colorXG, colorYG);
            resultB = getCountedColor(colorXB, colorYB);

            return Color.FromArgb(Clamp((int)resultR), Clamp((int)resultG), Clamp((int)resultB));
        }

        protected int getCountedColor(float colorX, float colorY)
        {
            return (int)Math.Sqrt((colorX * colorX + colorY + colorY));
        }
    }

    class SharpnessFilter: MatrixFilter
    {
        public SharpnessFilter()
        {
            kernel = new float[,] { {  0, -1,  0},
                                    { -1,  5, -1},
                                    {  0, -1,  0} };
        }
    }

    class EmbossingFilter : MatrixFilter
    {
        public EmbossingFilter()
        {
            kernel = new float[,] { { 0,  1,  0},
                                    { 1,  0, -1},
                                    { 0, -1,  0} };
        }

        public Bitmap processImage(Bitmap sourceImage, BackgroundWorker worker)
        {
            if (sourceImage == null)
                return null;
            Bitmap resultImage = new Bitmap(sourceImage.Width, sourceImage.Height);

            for (int i = 0; i < sourceImage.Width; i++)
            {
                worker.ReportProgress((int)((float)i / resultImage.Width * 50));
                if (worker.CancellationPending)
                    return null;

                for (int j = 0; j < sourceImage.Height; j++)
                {
                    resultImage.SetPixel(i, j, calculateNewPixelColorGrayScale(sourceImage, i, j));
                }
            }

            for (int i = 0; i < sourceImage.Width; i++)
            {
                worker.ReportProgress(50 + (int)((float)i / resultImage.Width * 50));
                if (worker.CancellationPending)
                    return null;

                for (int j = 0; j < sourceImage.Height; j++)
                {
                    resultImage.SetPixel(i, j, calculateNewPixelColor(resultImage, i, j));
                }
            }
            return resultImage;
        }

        protected Color calculateNewPixelColorGrayScale(Bitmap sourceImage, int x, int y)
        {
            Color sourceColor = sourceImage.GetPixel(x, y);
            int intensity = getIntensity(sourceColor.R, sourceColor.G, sourceColor.B);
            return Color.FromArgb(Clamp(intensity), Clamp(intensity), Clamp(intensity));
        }

        protected override Color calculateNewPixelColor(Bitmap sourceImage, int x, int y)
        {
            int radiusX = kernel.GetLength(0) / 2;
            int radiusY = kernel.GetLength(1) / 2;

            float resultR = 0, resultG = 0, resultB = 0;
            for (int l = -radiusY; l <= radiusY; l++)
                for (int k = -radiusX; k <= radiusX; k++)
                {
                    int idX = Clamp(x + k, 0, sourceImage.Width - 1);
                    int idY = Clamp(y + l, 0, sourceImage.Height - 1);
                    Color neighborColor = sourceImage.GetPixel(idX, idY);
                    resultR += neighborColor.R * kernel[k + radiusX, l + radiusY];
                    resultG += neighborColor.G * kernel[k + radiusX, l + radiusY];
                    resultB += neighborColor.B * kernel[k + radiusX, l + radiusY];
                }
            resultR = (resultR + 255) / 2;
            resultG = (resultG + 255) / 2;
            resultB = (resultB + 255) / 2;

            return Color.FromArgb(Clamp((int)resultR), Clamp((int)resultG), Clamp((int)resultB));
        }
    }

    class Sharpness2Filter : MatrixFilter
    {
        public Sharpness2Filter()
        {
            kernel = new float[,] { { -1, -1, -1},
                                    { -1,  9, -1},
                                    { -1, -1, -1} };
        }
    }

    class GrayWorld : Filters
    {
        public override Bitmap processImage(Bitmap sourceImage, BackgroundWorker worker)
        {
            if (sourceImage == null)
                return null;
            Bitmap resultImage = new Bitmap(sourceImage.Width, sourceImage.Height);

            double sumR = 0;
            double sumG = 0;
            double sumB = 0;
            int N = sourceImage.Width * sourceImage.Height;
            Color color;
            for (int i = 0; i < sourceImage.Width; i++)
                for (int j = 0; j < sourceImage.Height; j++)
                {
                    color = sourceImage.GetPixel(i, j);
                    sumR += color.R;
                    sumG += color.G;
                    sumB += color.B;
                }
            sumR /= N;
            sumG /= N;
            sumB /= N;
            double avg = (sumR + sumG + sumB) / 3;


            for (int i = 0; i < sourceImage.Width; i++)
            {
                worker.ReportProgress((int)((float)i / resultImage.Width * 100));
                if (worker.CancellationPending)
                    return null;

                for (int j = 0; j < sourceImage.Height; j++)
                {
                    resultImage.SetPixel(i, j, calculateNewPixelColor(sourceImage, i, j, avg, sumR, sumG, sumB));
                }
            }
            return resultImage;
        }

        protected override Color calculateNewPixelColor(Bitmap sourceImage, int x, int y) {
            return Color.FromArgb(255, 0, 0);
        }

        protected Color calculateNewPixelColor(Bitmap sourceImage, int x, int y, double avg, double sumR, double sumG, double sumB)
        {
            Color sourceColor = sourceImage.GetPixel(x, y);
            return Color.FromArgb(
                Clamp((int)(sourceColor.R * avg / sumR)),
                Clamp((int)(sourceColor.G * avg / sumG)),
                Clamp((int)(sourceColor.B * avg / sumB))
            );
        }
    }

    class Dilation : MatrixFilter
    {
        public Dilation()
        {
            kernel = new float[,] { { 0, 1, 0},
                                    { 1, 1, 1},
                                    { 0, 1, 0} };
        }

        protected override Color calculateNewPixelColor(Bitmap sourceImage, int x, int y)
        {
            int radiusX = kernel.GetLength(0) / 2;
            int radiusY = kernel.GetLength(1) / 2;

            Color maxColor = Color.FromArgb(0, 0, 0);
            for (int l = -radiusY; l <= radiusY; l++)
                for (int k = -radiusX; k <= radiusX; k++)
                {
                    int idX = Clamp(x + k, 0, sourceImage.Width - 1);
                    int idY = Clamp(y + l, 0, sourceImage.Height - 1);
                    Color neighborColor = sourceImage.GetPixel(idX, idY);
                    if ((kernel[k + radiusX, l + radiusY] == 1) && (neighborColor.R > maxColor.R))
                        maxColor = neighborColor;
                }

            return maxColor;
        }
    }

    class Erosion : MatrixFilter
    {
        public Erosion()
        {
            kernel = new float[,] { { 0, 1, 0},
                                    { 1, 1, 1},
                                    { 0, 1, 0} };
        }

        protected override Color calculateNewPixelColor(Bitmap sourceImage, int x, int y)
        {
            int radiusX = kernel.GetLength(0) / 2;
            int radiusY = kernel.GetLength(1) / 2;

            Color minColor = Color.FromArgb(255, 255, 255);
            for (int l = -radiusY; l <= radiusY; l++)
                for (int k = -radiusX; k <= radiusX; k++)
                {
                    int idX = Clamp(x + k, 0, sourceImage.Width - 1);
                    int idY = Clamp(y + l, 0, sourceImage.Height - 1);
                    Color neighborColor = sourceImage.GetPixel(idX, idY);
                    if ((kernel[k + radiusX, l + radiusY] == 1) && (neighborColor.R < minColor.R))
                        minColor = neighborColor;
                }

            return minColor;
        }
    }

    class Open : MatrixFilter
    {
        public Open()
        {
            kernel = new float[,] { { 0, 1, 0},
                                    { 1, 1, 1},
                                    { 0, 1, 0} };
        }

        protected Color calculateNewPixelColorDilation(Bitmap sourceImage, int x, int y)
        {
            int radiusX = kernel.GetLength(0) / 2;
            int radiusY = kernel.GetLength(1) / 2;

            Color maxColor = Color.FromArgb(0, 0, 0);
            for (int l = -radiusY; l <= radiusY; l++)
                for (int k = -radiusX; k <= radiusX; k++)
                {
                    int idX = Clamp(x + k, 0, sourceImage.Width - 1);
                    int idY = Clamp(y + l, 0, sourceImage.Height - 1);
                    Color neighborColor = sourceImage.GetPixel(idX, idY);
                    if ((kernel[k + radiusX, l + radiusY] == 1) && (neighborColor.R > maxColor.R))
                        maxColor = neighborColor;
                }

            return maxColor;
        }

        protected Color calculateNewPixelColorErosion(Bitmap sourceImage, int x, int y)
        {
            int radiusX = kernel.GetLength(0) / 2;
            int radiusY = kernel.GetLength(1) / 2;

            Color minColor = Color.FromArgb(255, 255, 255);
            for (int l = -radiusY; l <= radiusY; l++)
                for (int k = -radiusX; k <= radiusX; k++)
                {
                    int idX = Clamp(x + k, 0, sourceImage.Width - 1);
                    int idY = Clamp(y + l, 0, sourceImage.Height - 1);
                    Color neighborColor = sourceImage.GetPixel(idX, idY);
                    if ((kernel[k + radiusX, l + radiusY] == 1) && (neighborColor.R < minColor.R))
                        minColor = neighborColor;
                }

            return minColor;
        }

        public override Bitmap processImage(Bitmap sourceImage, BackgroundWorker worker)
        {
            if (sourceImage == null)
                return null;
            Bitmap resultImage = new Bitmap(sourceImage.Width, sourceImage.Height);
            for (int i = 0; i < sourceImage.Width; i++)
            {
                worker.ReportProgress((int)((float)i / resultImage.Width * 50));
                if (worker.CancellationPending)
                    return null;

                for (int j = 0; j < sourceImage.Height; j++)
                {
                    resultImage.SetPixel(i, j, calculateNewPixelColorErosion(sourceImage, i, j));
                }
            }

            Bitmap resultImage2 = new Bitmap(resultImage.Width, resultImage.Height);
            for (int i = 0; i < resultImage.Width; i++)
            {
                worker.ReportProgress(50 + (int)((float)i / resultImage2.Width * 50));
                if (worker.CancellationPending)
                    return null;

                for (int j = 0; j < resultImage.Height; j++)
                {
                    resultImage2.SetPixel(i, j, calculateNewPixelColorDilation(resultImage, i, j));
                }
            }
            return resultImage2;
        }
    }

    class Close : MatrixFilter
    {
        public Close()
        {
            kernel = new float[,] { { 0, 1, 0},
                                    { 1, 1, 1},
                                    { 0, 1, 0} };
        }

        protected Color calculateNewPixelColorDilation(Bitmap sourceImage, int x, int y)
        {
            int radiusX = kernel.GetLength(0) / 2;
            int radiusY = kernel.GetLength(1) / 2;

            Color maxColor = Color.FromArgb(0, 0, 0);
            for (int l = -radiusY; l <= radiusY; l++)
                for (int k = -radiusX; k <= radiusX; k++)
                {
                    int idX = Clamp(x + k, 0, sourceImage.Width - 1);
                    int idY = Clamp(y + l, 0, sourceImage.Height - 1);
                    Color neighborColor = sourceImage.GetPixel(idX, idY);
                    if ((kernel[k + radiusX, l + radiusY] == 1) && (neighborColor.R > maxColor.R))
                        maxColor = neighborColor;
                }

            return maxColor;
        }

        protected Color calculateNewPixelColorErosion(Bitmap sourceImage, int x, int y)
        {
            int radiusX = kernel.GetLength(0) / 2;
            int radiusY = kernel.GetLength(1) / 2;

            Color minColor = Color.FromArgb(255, 255, 255);
            for (int l = -radiusY; l <= radiusY; l++)
                for (int k = -radiusX; k <= radiusX; k++)
                {
                    int idX = Clamp(x + k, 0, sourceImage.Width - 1);
                    int idY = Clamp(y + l, 0, sourceImage.Height - 1);
                    Color neighborColor = sourceImage.GetPixel(idX, idY);
                    if ((kernel[k + radiusX, l + radiusY] == 1) && (neighborColor.R < minColor.R))
                        minColor = neighborColor;
                }

            return minColor;
        }

        public override Bitmap processImage(Bitmap sourceImage, BackgroundWorker worker)
        {
            if (sourceImage == null)
                return null;
            Bitmap resultImage = new Bitmap(sourceImage.Width, sourceImage.Height);
            for (int i = 0; i < sourceImage.Width; i++)
            {
                worker.ReportProgress((int)((float)i / resultImage.Width * 50));
                if (worker.CancellationPending)
                    return null;

                for (int j = 0; j < sourceImage.Height; j++)
                {
                    resultImage.SetPixel(i, j, calculateNewPixelColorDilation(sourceImage, i, j));
                }
            }

            Bitmap resultImage2 = new Bitmap(sourceImage.Width, sourceImage.Height);
            for (int i = 0; i < resultImage.Width; i++)
            {
                worker.ReportProgress(50 + (int)((float)i / resultImage2.Width * 50));
                if (worker.CancellationPending)
                    return null;

                for (int j = 0; j < resultImage.Height; j++)
                {
                    resultImage2.SetPixel(i, j, calculateNewPixelColorErosion(resultImage, i, j));
                }
            }
            return resultImage2;
        }
    }

    class Grad : MatrixFilter
    {
        public Grad()
        {
            kernel = new float[,] { { 0, 1, 0},
                                    { 1, 1, 1},
                                    { 0, 1, 0} };
        }

        protected Color calculateNewPixelColorDilation(Bitmap sourceImage, int x, int y)
        {
            int radiusX = kernel.GetLength(0) / 2;
            int radiusY = kernel.GetLength(1) / 2;

            Color maxColor = Color.FromArgb(0, 0, 0);
            for (int l = -radiusY; l <= radiusY; l++)
                for (int k = -radiusX; k <= radiusX; k++)
                {
                    int idX = Clamp(x + k, 0, sourceImage.Width - 1);
                    int idY = Clamp(y + l, 0, sourceImage.Height - 1);
                    Color neighborColor = sourceImage.GetPixel(idX, idY);
                    if ((kernel[k + radiusX, l + radiusY] == 1) && (neighborColor.R > maxColor.R))
                        maxColor = neighborColor;
                }

            return maxColor;
        }

        protected Color calculateNewPixelColorErosion(Bitmap sourceImage, int x, int y)
        {
            int radiusX = kernel.GetLength(0) / 2;
            int radiusY = kernel.GetLength(1) / 2;

            Color minColor = Color.FromArgb(255, 255, 255);
            for (int l = -radiusY; l <= radiusY; l++)
                for (int k = -radiusX; k <= radiusX; k++)
                {
                    int idX = Clamp(x + k, 0, sourceImage.Width - 1);
                    int idY = Clamp(y + l, 0, sourceImage.Height - 1);
                    Color neighborColor = sourceImage.GetPixel(idX, idY);
                    if ((kernel[k + radiusX, l + radiusY] == 1) && (neighborColor.R < minColor.R))
                        minColor = neighborColor;
                }

            return minColor;
        }

        public override Bitmap processImage(Bitmap sourceImage, BackgroundWorker worker)
        {
            if (sourceImage == null)
                return null;
            Bitmap resultImage = new Bitmap(sourceImage.Width, sourceImage.Height);
            for (int i = 0; i < sourceImage.Width; i++)
            {
                worker.ReportProgress((int)((float)i / resultImage.Width * 33));
                if (worker.CancellationPending)
                    return null;

                for (int j = 0; j < sourceImage.Height; j++)
                {
                    resultImage.SetPixel(i, j, calculateNewPixelColorDilation(sourceImage, i, j));
                }
            }

            Bitmap resultImage2 = new Bitmap(sourceImage.Width, sourceImage.Height);
            for (int i = 0; i < sourceImage.Width; i++)
            {
                worker.ReportProgress(33 + (int)((float)i / resultImage2.Width * 33));
                if (worker.CancellationPending)
                    return null;

                for (int j = 0; j < sourceImage.Height; j++)
                {
                    resultImage2.SetPixel(i, j, calculateNewPixelColorErosion(sourceImage, i, j));
                }
            }

            Bitmap resultImage3 = new Bitmap(sourceImage.Width, sourceImage.Height);
            for (int i = 0; i < sourceImage.Width; i++)
            {
                worker.ReportProgress(66 + (int)((float)i / resultImage2.Width * 33));
                if (worker.CancellationPending)
                    return null;

                for (int j = 0; j < sourceImage.Height; j++)
                {
                    int resultR = Clamp(resultImage.GetPixel(i, j).R - resultImage2.GetPixel(i, j).R);
                    int resultG = Clamp(resultImage.GetPixel(i, j).G - resultImage2.GetPixel(i, j).G);
                    int resultB = Clamp(resultImage.GetPixel(i, j).B - resultImage2.GetPixel(i, j).B);
                    resultImage3.SetPixel(i, j, Color.FromArgb(resultR, resultG, resultB));
                }
            }

            return resultImage3;
        }
    }

    class Median : MatrixFilter
    {
        protected override Color calculateNewPixelColor(Bitmap sourceImage, int x, int y)
        {
            int radius = 1;
            int new_radius = radius * 2 + 1;
            int size = new_radius * new_radius;

            int[] arrR = new int[size];
            int[] arrG = new int[size];
            int[] arrB = new int[size];
            for (int l = -radius; l <= radius; l++)
                for (int k = -radius; k <= radius; k++)
                {
                    int idX = Clamp(x + k, 0, sourceImage.Width - 1);
                    int idY = Clamp(y + l, 0, sourceImage.Height - 1);
                    Color neighborColor = sourceImage.GetPixel(idX, idY);
                    arrR[k + radius + (l + radius) * new_radius] = neighborColor.R;
                    arrG[k + radius + (l + radius) * new_radius] = neighborColor.G;
                    arrB[k + radius + (l + radius) * new_radius] = neighborColor.B;
                }
            Array.Sort(arrR);
            Array.Sort(arrG);
            Array.Sort(arrB);

            int med = size / 2;
            return Color.FromArgb(arrR[med], arrG[med], arrB[med]);
        }
    }
}