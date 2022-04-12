namespace Inversion
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Click(object sender, EventArgs e)
        {
            this.BackColor = Color.Red;
        }

        public static int Clamp(int value, int min, int max)
        {
            if (value < min)
                return min;
            if (value > max)
                return max;
            return value;
        }

        public static Bitmap inversion(Bitmap source)
        {
            Color color;
            for (int x = 0; x < source.Width; x++)
                for (int y = 0; y < source.Height; y++)
                {
                    color = source.GetPixel(x, y);
                    Color new_color = Color.FromArgb(255 - color.R, 255 - color.G, 255 - color.B);
                    source.SetPixel(x, y, new_color);
                }

            return source;
        }

        public static Bitmap shade_of_gray(Bitmap source)
        {
            Color color;
            for (int x = 0; x < source.Width; x++)
                for (int y = 0; y < source.Height; y++)
                {
                    color = source.GetPixel(x, y);
                    byte new_color = (byte)(.299 * color.R + .587 * color.G + .114 * color.B);
                    source.SetPixel(x, y, Color.FromArgb(new_color, new_color, new_color));
                }

            return source;
        }

        public static Bitmap increase_brightness(Bitmap source, int constant)
        {
            Color color;
            for (int x = 0; x < source.Width; x++)
                for (int y = 0; y < source.Height; y++)
                {
                    color = source.GetPixel(x, y);
                    int R = Clamp(color.R + constant, 0, 255);
                    int G = Clamp(color.G + constant, 0, 255);
                    int B = Clamp(color.B + constant, 0, 255);

                    source.SetPixel(x, y, Color.FromArgb(R, G, B));
                }

            return source;
        }

        public static Bitmap convolution(Bitmap source, int[,] arr)
        {
            Bitmap image = new Bitmap(source);

            int radiusX = arr.GetLength(0) / 2;
            int radiusY = arr.GetLength(1) / 2;

            Color color;
            for (int x = 0; x < source.Width; x++)
                for (int y = 0; y < source.Height; y++)
                {
                    int resultR = 0;
                    int resultG = 0;
                    int resultB = 0;
                    for (int l = -radiusY; l <= radiusY; l++)
                        for (int k = -radiusX; k <= radiusX; k++)
                        {
                            int idX = Clamp(x + k, 0, source.Width - 1);
                            int idY = Clamp(y + l, 0, source.Height - 1);

                            color = source.GetPixel(idX, idY);

                            resultR += color.R * arr[k + radiusX, l + radiusY];
                            resultG += color.G * arr[k + radiusX, l + radiusY];
                            resultB += color.B * arr[k + radiusX, l + radiusY];
                        }
                    image.SetPixel(x, y, Color.FromArgb(Clamp((int)resultR, 0, 255),
                                                        Clamp((int)resultG, 0, 255),
                                                        Clamp((int)resultB, 0, 255)));
                }

            return image;
        }

        public static Color MotionBlur(Bitmap sourceImage, int x, int y, float[,] arr)
        {
            int radiusX = 4;
            int radiusY = 4;

            float resultR = 0;
            float resultG = 0;
            float resultB = 0;

            for (int l = -radiusY; l <= radiusY; l++)
            {
                for (int k = -radiusX; k <= radiusX; k++)
                {
                    int idX = Clamp(x + k, 0, sourceImage.Width - 1);
                    int idY = Clamp(y + l, 0, sourceImage.Height - 1);
                    Color neighbourColor = sourceImage.GetPixel(idX, idY);

                    resultR += neighbourColor.R * arr[k + radiusX, l + radiusY];
                    resultG += neighbourColor.G * arr[k + radiusX, l + radiusY];
                    resultB += neighbourColor.B * arr[k + radiusX, l + radiusY];
                }
            }
            Color resultColor = Color.FromArgb(Clamp((int)resultR, 0, 255), Clamp((int)resultG, 0, 255), Clamp((int)resultB, 0, 255));
            return resultColor;
        }

        public static Bitmap gray_world(Bitmap source)
        {
            double sumR = 0;
            double sumG = 0;
            double sumB = 0;
            int N = source.Width * source.Height;
            Color color;
            for (int x = 0; x < source.Width; x++)
                for (int y = 0; y < source.Height; y++)
                {
                    color = source.GetPixel(x, y);
                    sumR += color.R;
                    sumG += color.G;
                    sumB += color.B;
                }
            sumR /= N;
            sumG /= N;
            sumB /= N;
            double avg = (sumR + sumG + sumB) / 3;

            int R;
            int G;
            int B;
            for (int x = 0; x < source.Width; x++)
                for (int y = 0; y < source.Height; y++)
                {
                    color = source.GetPixel(x, y);
                    R = (int)(color.R * avg / sumR);
                    G = (int)(color.G * avg / sumG);
                    B = (int)(color.B * avg / sumB);
                    source.SetPixel(x, y, Color.FromArgb(Clamp(R, 0, 255), Clamp(G, 0, 255), Clamp(B, 0, 255)));
                }

            return source;
        }

        public static Bitmap autolevels(Bitmap source)
        {
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
            for (int x = 0; x < source.Width; x++)
                for (int y = 0; y < source.Height; y++)
                {
                    color = source.GetPixel(x, y);

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

            for (int x = 0; x < source.Width; x++)
                for (int y = 0; y < source.Height; y++)
                {
                    color = source.GetPixel(x, y);


                    source.SetPixel(x, y, Color.FromArgb((color.R - Rmin) * 255 / (Rmax - Rmin),
                                                         (color.G - Gmin) * 255 / (Gmax - Gmin),
                                                         (color.B - Bmin) * 255 / (Bmax - Bmin)));
                }

            return source;
        }

        public static Bitmap perfect_reflector(Bitmap source)
        {
            int Rmax = 0;
            int Gmax = 0;
            int Bmax = 0;

            Color color;
            for (int x = 0; x < source.Width; x++)
                for (int y = 0; y < source.Height; y++)
                {
                    color = source.GetPixel(x, y);

                    if (color.R > Rmax)
                        Rmax = color.R;

                    if (color.G > Gmax)
                        Gmax = color.G;

                    if (color.B > Bmax)
                        Bmax = color.B;
                }

            for (int x = 0; x < source.Width; x++)
                for (int y = 0; y < source.Height; y++)
                {
                    color = source.GetPixel(x, y);

                    source.SetPixel(x, y, Color.FromArgb((int)(color.R * 255.0 / Rmax),
                                                         (int)(color.G * 255.0 / Gmax),
                                                         (int)(color.B * 255.0 / Bmax)));
                }

            return source;
        }

        public static Bitmap dilation(Bitmap source)
        {
            Bitmap image = new Bitmap(source.Width, source.Height);

            int[,] arr = {{ 0, 1, 0 },
                          { 1, 1, 1 },
                          { 0, 1, 0 }};
            int radius = 3;
            int new_radius = radius / 2;
            for (int y = 0; y < source.Height; y++)
                for (int x = 0; x < source.Width; x++)
                {
                    Color max = Color.FromArgb(0, 0, 0);
                    for (int j = -new_radius; j <= new_radius; j++)
                        for (int i = -new_radius; i <= new_radius; i++)
                        {
                            Color color = source.GetPixel(Clamp(x + i, 0, source.Width - 1), Clamp(y + j, 0, source.Height - 1));
                            if ((arr[i + new_radius, j + new_radius] == 1) && (color.R > max.R))
                                max = color;
                        }
                    image.SetPixel(x, y, max);
                }

            return image;
        }

        public static Bitmap erosion(Bitmap source)
        {
            Bitmap image = new Bitmap(source.Width, source.Height);

            int[,] arr = {{ 0, 1, 0 },
                          { 1, 1, 1 },
                          { 0, 1, 0 }};
            int radius = 3;
            int new_radius = radius / 2;
            for (int y = 0; y < source.Height; y++)
                for (int x = 0; x < source.Width; x++)
                {
                    Color max = Color.FromArgb(255, 255, 255);
                    for (int j = -new_radius; j <= new_radius; j++)
                        for (int i = -new_radius; i <= new_radius; i++)
                        {
                            Color color = source.GetPixel(Clamp(x + i, 0, source.Width - 1), Clamp(y + j, 0, source.Height - 1));
                            if ((arr[i + new_radius, j + new_radius] == 1) && (color.R < max.R))
                                max = color;
                        }
                    image.SetPixel(x, y, max);
                }

            return image;
        }

        public static Bitmap median(Bitmap source)
        {
            /*Bitmap image = new Bitmap(source);

            Color color;
            int tmp;
            int new_radius = 2 * radius + 1;
            for (int x = 0; x < source.Width; x++)
                for (int y = 0; y < source.Height; y++)
                {
                    int[] arrR = new int[new_radius * new_radius];
                    int[] arrG = new int[new_radius * new_radius];
                    int[] arrB = new int[new_radius * new_radius];
                    for (int i = -radius; i <= radius; i++)
                        for (int j = -radius; j <= radius; j++)
                        {
                            if ((0 <= x + i) && (x + i < source.Width) && (0 <= y + j) && (y + j < source.Height))
                                color = source.GetPixel(x + i, y + j);
                            else
                                color = Color.FromArgb(0, 0, 0);
                            arrR[i + 1 + (j + 1) * radius] = color.R;
                            arrG[i + 1 + (j + 1) * radius] = color.G;
                            arrB[i + 1 + (j + 1) * radius] = color.B;
                        }
                    for (int i = 0; i < new_radius * new_radius - 1; i++)
                        for (int j = 0; j < new_radius * new_radius - i - 1; j++)
                        {
                            if (arrR[j] > arrR[j + 1])
                            {
                                tmp = arrR[j];
                                arrR[j] = arrR[j + 1];
                                arrR[j + 1] = tmp;
                            }
                            if (arrG[j] > arrG[j + 1])
                            {
                                tmp = arrG[j];
                                arrG[j] = arrG[j + 1];
                                arrG[j + 1] = tmp;
                            }
                            if (arrB[j] > arrB[j + 1])
                            {
                                tmp = arrB[j];
                                arrB[j] = arrB[j + 1];
                                arrB[j + 1] = tmp;
                            }
                        }

                    int index = new_radius * new_radius / 2 + 1;
                    image.SetPixel(x, y, Color.FromArgb(arrR[index], arrG[index], arrB[index]));
                }

            return image;*/
            Bitmap image = new Bitmap(source.Width, source.Height);

            Color tmp;
            int radius = 1;
            int new_radius = 2 * radius + 1;
            for (int y = 0; y < source.Height; y++)
                for (int x = 0; x < source.Width; x++)
                {
                    Color[] arr = new Color[new_radius * new_radius];
                    for (int j = -radius; j <= radius; j++)
                        for (int i = -radius; i <= radius; i++)
                        {
                            Color color = source.GetPixel(Clamp(x + i, 0, source.Width - 1), Clamp(y + j, 0, source.Height - 1));
                            arr[i + 1 + (j + 1) * radius] = color;
                        }
                    for (int i = 0; i < new_radius * new_radius - 1; i++)
                        for (int j = 0; j < new_radius * new_radius - i - 1; j++)
                        {
                            if (arr[j].R > arr[j + 1].R)
                            {
                                tmp = arr[j];
                                arr[j] = arr[j + 1];
                                arr[j + 1] = tmp;
                            }
                        }

                    image.SetPixel(x, y, Color.FromArgb(arr[4].R, arr[4].G, arr[4].B));
                }

            return image;
        }

        public static Bitmap Sobel(Bitmap source)
        {
            Bitmap image = new Bitmap(source.Width, source.Height);

            Color oldColor, newColor;
            float[,] G_y = { { -1, -2, -1 },
                             { 0, 0, 0 },
                             { 1, 2, 1 } };
            float[,] G_x = { { -1, 0, 1 },
                             { -2, 0, 2 },
                             { -1, 0, 1 } };
            int radius = 1;
            int idX, idY;
            float ColorXR, ColorXG, ColorXB;
            float ColorYR, ColorYG, ColorYB;
            float ColorR, ColorG, ColorB;
            for (int i = 0; i < source.Width; i++)
            {
                for (int j = 0; j < source.Height; j++)
                {
                    ColorXR = 0; ColorXG = 0; ColorXB = 0;
                    ColorYR = 0; ColorYG = 0; ColorYB = 0;
                    for (int k = -radius; k <= radius; k++)
                    {
                        for (int l = -radius; l <= radius; l++)
                        {
                            idX = Clamp(i + k, 0, source.Width - 1);
                            idY = Clamp(j + l, 0, source.Height - 1);
                            oldColor = source.GetPixel(idX, idY);
                            ColorXR += G_x[radius + k, radius + l] * oldColor.R;
                            ColorXG += G_x[radius + k, radius + l] * oldColor.G;
                            ColorXB += G_x[radius + k, radius + l] * oldColor.B;
                            ColorYR += G_y[radius + k, radius + l] * oldColor.R;
                            ColorYG += G_y[radius + k, radius + l] * oldColor.G;
                            ColorYB += G_y[radius + k, radius + l] * oldColor.B;
                        }
                    }
                    ColorR = (float)Math.Sqrt((ColorXR * ColorXR + ColorYR * ColorYR));
                    ColorG = (float)Math.Sqrt((ColorXG * ColorXG + ColorYG * ColorYG));
                    ColorB = (float)Math.Sqrt((ColorXB * ColorXB + ColorYB * ColorYB));
                    newColor = Color.FromArgb(Clamp((int)ColorR, 0, 255),
                    Clamp((int)ColorG, 0, 255),
                    Clamp((int)ColorB, 0, 255));
                    image.SetPixel(i, j, newColor);
                }
            }

            return image;
        }

        public static Bitmap Sharr(Bitmap source)
        {
            Bitmap image = new Bitmap(source.Width, source.Height);

            Color oldColor, newColor;
            float[,] G_y = { { -3, -10, -3 },
                             { 0, 0, 0 },
                             { 3, 10, 3 } };
            float[,] G_x = { { -3, 0, 3 },
                             { -10, 0, 10 },
                             { -3, 0, 3 } };
            int radius = 1;
            int idX, idY;
            float ColorXR, ColorXG, ColorXB;
            float ColorYR, ColorYG, ColorYB;
            float ColorR, ColorG, ColorB;
            for (int i = 0; i < source.Width; i++)
            {
                for (int j = 0; j < source.Height; j++)
                {
                    ColorXR = 0; ColorXG = 0; ColorXB = 0;
                    ColorYR = 0; ColorYG = 0; ColorYB = 0;
                    for (int k = -radius; k <= radius; k++)
                    {
                        for (int l = -radius; l <= radius; l++)
                        {
                            idX = Clamp(i + k, 0, source.Width - 1);
                            idY = Clamp(j + l, 0, source.Height - 1);
                            oldColor = source.GetPixel(idX, idY);
                            ColorXR += G_x[radius + k, radius + l] * oldColor.R;
                            ColorXG += G_x[radius + k, radius + l] * oldColor.G;
                            ColorXB += G_x[radius + k, radius + l] * oldColor.B;
                            ColorYR += G_y[radius + k, radius + l] * oldColor.R;
                            ColorYG += G_y[radius + k, radius + l] * oldColor.G;
                            ColorYB += G_y[radius + k, radius + l] * oldColor.B;
                        }
                    }
                    ColorR = (float)Math.Sqrt((ColorXR * ColorXR + ColorYR * ColorYR));
                    ColorG = (float)Math.Sqrt((ColorXG * ColorXG + ColorYG * ColorYG));
                    ColorB = (float)Math.Sqrt((ColorXB * ColorXB + ColorYB * ColorYB));
                    newColor = Color.FromArgb(Clamp((int)ColorR, 0, 255),
                    Clamp((int)ColorG, 0, 255),
                    Clamp((int)ColorB, 0, 255));
                    image.SetPixel(i, j, newColor);
                }
            }

            return image;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Bitmap image = new Bitmap("C:\\Users\\vladk\\Downloads\\Telegram Desktop\\1.jpg");
           
            Bitmap source = new Bitmap(image);

            /* -----------------------------------------------------6 task----------------------------------------------------- */

            //int[,] arr = {{ 0, 1, 0 },
            //              { -1, 0, 1 },
            //              { 0, -1, 0 }};          
            //source = convolution(source, arr);
            //source = shade_of_gray(source);
            //source = increase_brightness(source, 100);

            /* -----------------------------------------------------8 task----------------------------------------------------- */

            //source = gray_world(source);

            /* -----------------------------------------------------9 task----------------------------------------------------- */

            //source = autolevels(source);

            /* -----------------------------------------------------10 task----------------------------------------------------- */

            //source = perfect_reflector(source);

            /* -----------------------------------------------------11 task----------------------------------------------------- */

            //source = dilation(source);

            /* -----------------------------------------------------12 task----------------------------------------------------- */

            //source = erosion(source);

            /* -----------------------------------------------------13 task----------------------------------------------------- */
            /* не готов */

            //source = median(source);

            /* -----------------------------------------------------14 task----------------------------------------------------- */

            //source = Sobel(source);

            /* -----------------------------------------------------15 task----------------------------------------------------- */

            source = Sharr(source);

            pictureBox1.Image = image;
            pictureBox2.Image = source;
        }
    }
}