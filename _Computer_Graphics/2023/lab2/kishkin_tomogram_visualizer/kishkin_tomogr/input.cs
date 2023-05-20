using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace kishkin_tomogr_input
{
    class Bin
    {
        public static int X, Y, Z;
        public static short[] array;

        public Bin() { }

        public void readBIN(string path)
        {
            if (File.Exists(path))
            {
                BinaryReader reader = new BinaryReader(File.Open(path, FileMode.Open));

                X = reader.ReadInt32();
                Y = reader.ReadInt32();
                Z = reader.ReadInt32();

                int arraySize = X * Y * Z;
                array = new short[arraySize];
                for (int i = 0; i < arraySize; ++i)
                {
                    array[i] = reader.ReadInt16();
                }
            }
        }

        /*public void rotateTomogram(Boolean isRotate)
        {
            if (isRotate)
            {
                Int32 tmpX = Z, tmpY = X, tmpZ = Y;
                X = tmpX; Y = tmpY; Z = tmpZ;
            }
            else
            {
                Int32 tmpX = Y, tmpY = Z, tmpZ = X;
                X = tmpX; Y = tmpY; Z = tmpZ;
            }
        }*/
    }
}
