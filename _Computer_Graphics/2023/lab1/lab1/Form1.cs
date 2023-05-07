using Filters_Kishkin;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;

namespace lab1
{
    public partial class Form1 : Form
    {
        Bitmap image;

        public Form1()
        {
            InitializeComponent();
        }

        private void менюToolStripMenuItem_Click(object sender, EventArgs e)
        {

        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {
            if (image == null)
                openDialog();
            else
                saveDialog();
        }

        private void открытьToolStripMenuItem_Click(object sender, EventArgs e)
        {
            openDialog();
        }

        private void openDialog()
        {
            OpenFileDialog dialog = new OpenFileDialog();
            dialog.Filter = "Image files|*.png;*.jpg;*.bmp|All files(*.*)|*.*";
            if (dialog.ShowDialog() == DialogResult.OK)
            {
                image = new Bitmap(dialog.FileName);
                pictureBox1.Image = image;
                pictureBox1.Refresh();
            }
        }

        private void сохранитьToolStripMenuItem_Click(object sender, EventArgs e)
        {
            saveDialog();
        }

        private void saveDialog()
        {
            SaveFileDialog dialog = new SaveFileDialog();
            dialog.Filter = "Image files|*.png;*.jpg;*.bmp|All files(*.*)|*.*";
            ImageFormat format = ImageFormat.Png;
            if (dialog.ShowDialog() == DialogResult.OK)
            {
                string extension = System.IO.Path.GetExtension(dialog.FileName);
                switch(extension)
                {
                    case ".jpg":
                        format = ImageFormat.Jpeg;
                        break;
                }
                pictureBox1.Image.Save(dialog.FileName, format);
            }
        }

        private void инверсияToolStripMenuItem_Click(object sender, EventArgs e)
        {
            InvertFilter filter = new InvertFilter();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        private void backgroundWorker1_DoWork(object sender, DoWorkEventArgs e)
        {
            Bitmap newImage = ((Filters)e.Argument).processImage(image, backgroundWorker1);
            if (backgroundWorker1.CancellationPending != true)
                image = newImage;
        }

        private void backgroundWorker1_ProgressChanged(object sender, ProgressChangedEventArgs e)
        {
            progressBar1.Value = e.ProgressPercentage;
        }

        private void backgroundWorker1_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            if (!e.Cancelled)
            {
                pictureBox1.Image = image;
                pictureBox1.Refresh();
            }
            progressBar1.Value = 0;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            backgroundWorker1.CancelAsync();
        }

        private void progressBar1_Click(object sender, EventArgs e)
        {

        }

        /* ===== POINT FILTERS START ===== POINT FILTERS START ===== POINT FILTERS START ===== POINT FILTERS START ===== POINT FILTERS START ===== */

        private void grayScaleвОттенкахСерогоToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Filters filter = new GrayScaleFilter();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        private void сепияToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Filters filter = new SepiaFilter();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        private void яркостьToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Filters filter = new BrightnessFilter();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        private void серыйМирToolStripMenuItem_Click(object sender, EventArgs e)
        {
            GrayWorld filter = new GrayWorld();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        private void grayScaleToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Filters filter = new HalfGrayScaleFilter();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        /* ===== POINT FILTERS END ===== POINT FILTERS END ===== POINT FILTERS END ===== POINT FILTERS END ===== POINT FILTERS END ===== */

        /* ===== MATRIX FILTERS START ===== MATRIX FILTERS START ===== MATRIX FILTERS START ===== MATRIX FILTERS START ===== MATRIX FILTERS START ===== */

        private void размытиеToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Filters filter = new BlueFilter();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        private void размытиеПоГауссуToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Filters filter = new GaussianFilter();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        private void операторСобеляToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Filters filter = new SobelFilter();
            backgroundWorker1.RunWorkerAsync(filter);
        }
        private void резкостьToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Filters filter = new SharpnessFilter();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        private void тиснениеToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Filters filter = new EmbossingFilter();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        private void резкость2ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Filters filter = new Sharpness2Filter();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        private void переменосПоXВправоToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Filters filter = new MoveXtoRigthFilter();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        private void стеклоToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Filters filter = new GlassFilter();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        private void dilationToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Filters filter = new Dilation();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        private void erosionToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Filters filter = new Erosion();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        private void openingToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Filters filter = new Open();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        private void closingToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Filters filter = new Close();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        private void gradToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Filters filter = new Grad();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        private void medianToolStripMenuItem1_Click_1(object sender, EventArgs e)
        {
            Filters filter = new Median();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        private void линейнаяКоррекцияToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Filters filter = new LinearCorrection();
            backgroundWorker1.RunWorkerAsync(filter);
        }

        /* ===== MATRIX FILTERS END ===== MATRIX FILTERS END ===== MATRIX FILTERS END ===== MATRIX FILTERS END ===== MATRIX FILTERS END ===== */
    }
}
