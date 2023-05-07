using kishkin_tomogr_input;
using kishkin_tomogr_output;

using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using OpenTK;


namespace kishkin_tomogr
{
    public partial class Form1 : Form
    {
        bool loaded = false;
        Bin bin = new Bin();
        kishkin_tomogr_output.View view = new kishkin_tomogr_output.View();
        int currentLayer;

        int FrameCount;
        DateTime NextFPSUpdate = DateTime.Now.AddSeconds(1);

        bool needReload = false;

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            Application.Idle += Application_Idle;
        }

        private void открытьToolStripMenuItem_Click(object sender, EventArgs e)
        {
            OpenFileDialog dialog = new OpenFileDialog();
            if (dialog.ShowDialog() == DialogResult.OK) 
            {
                string str = dialog.FileName;
                bin.readBIN(str);
                view.SetupView(glControl1.Width, glControl1.Height);
                loaded = true;
                glControl1.Invalidate();

                trackBar1.Maximum = bin.getZ() - 1;
            }
        }

        private void glControl1_Paint(object sender, PaintEventArgs e)
        {            
            if (loaded)
            {
                
                if (checkBox1.Checked)
                {
                    /* Для визуализации томограммы с помощью отрисовки текстуры.
                       Текущий слой томограммы визуализируется как один большой четырехугольник,
                       на который изображение слоя накладывается как текстура аппаратной билинейной интерполяцией */
                    if (needReload)
                    {
                        view.generateTextureImage(currentLayer, trackBar2.Value, trackBar3.Value);
                        view.Load2DTexture();
                        needReload = false;
                    }
                    view.drawTexture();
                } else
                {
                    /* Для визуализации томограммы с помощью отрисовки четырехугольников, 
                       вершинами которых являеются центры вокселов текущего слоя регулярной воксельной сетки. 
                       Цвет формируется на центральном процессоре и отрисовывается с помощью функции GL.Benig(BeginMode.Quads) */
                    view.DrawQuards(currentLayer, trackBar2.Value, trackBar3.Value);
                    glControl1.SwapBuffers();
                }
                glControl1.SwapBuffers();
            }
        }

        private void trackBar1_Scroll(object sender, EventArgs e)
        {
            currentLayer = trackBar1.Value;
            needReload = true;

            if (checkBox1.Checked == false)
            {
                view.DrawQuards(currentLayer, trackBar2.Value, trackBar3.Value);
                glControl1.SwapBuffers();
            }
        }

        void Application_Idle(object sender, EventArgs e)
        {
            while (glControl1.IsIdle)
            {
                displayFPS();
                glControl1.Invalidate();
            }
        }

        void displayFPS()
        {
            if (DateTime.Now >= NextFPSUpdate)
            {
                this.Text = String.Format("CT Visualizer (fps={0})", FrameCount);
                NextFPSUpdate = DateTime.Now.AddSeconds(1);
                FrameCount = 0;
            }
            FrameCount++;
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }
    }
}
