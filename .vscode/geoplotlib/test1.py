 public static string HttpUploadFile(string url,string path, Form1 form1, Form1.UpLoadDelgate upLoadDelgate)
        {
            System.Net.ServicePointManager.Expect100Continue = false;
            HttpWebRequest request = WebRequest.Create(url) as HttpWebRequest;
            CookieContainer cookieContainer = new CookieContainer();
            request.CookieContainer = cookieContainer;
            request.AllowAutoRedirect = true;
            request.Method = "POST";
            string boundary = DateTime.Now.Ticks.ToString("X");
            request.ContentType = "multipart/form-data;charset=utf-8;boundary=" + boundary;
            byte[] itemBoundaryBytes = Encoding.UTF8.GetBytes("\r\n--" + boundary + "\r\n");
            byte[] endBoundaryBytes = Encoding.UTF8.GetBytes("\r\n--" + boundary + "--\r\n");
            int pos = path.LastIndexOf("\\");
            string fileName = path.Substring(pos + 1);
            StringBuilder stringBuilder = new StringBuilder(string.Format("Content-Disposition:form-data;name=\"fileName\";filename=\"{0}\"\r\nContent-Type:application/octet-stream\r\n\r\n", fileName));
            byte[] postHeaderBytes = Encoding.UTF8.GetBytes(stringBuilder.ToString());
            FileStream fs = new FileStream(path, FileMode.Open, FileAccess.Read);
            BinaryReader binaryReader = new BinaryReader(fs);
            long fileLength = fs.Length;
            long length = fileLength + postHeaderBytes.Length + endBoundaryBytes.Length;
            int bufferLength = 1024;
            byte[] bArr = new byte[bufferLength];
            long offset = 0;
            DateTime startTime = DateTime.Now;
            int size= binaryReader.Read(bArr, 0, bufferLength);
            Stream postStream = request.GetRequestStream();
            postStream.Write(itemBoundaryBytes, 0, itemBoundaryBytes.Length);
            postStream.Write(postHeaderBytes, 0, postHeaderBytes.Length);
            TranState tranState = new TranState();
            int count = 0;
            while (size > 0)
            {
                postStream.Write(bArr, 0, bArr.Length);
                offset += size;
                int Value = (int)Math.Round((offset * 100.0 / length), MidpointRounding.AwayFromZero);
                tranState.PbValue = Value;
                TimeSpan span = DateTime.Now - startTime;
                double second = span.TotalSeconds;
                string Text = "已用时：" + second.ToString("F2") + "秒";
                tranState.LblState = Text;
                if (second > 0.001)
                {
                    string lblSpeed= " 平均速度：" + (offset / 1024 / second).ToString("0.00") + "KB/秒";
                    tranState.LblSpeed = lblSpeed;
                }
                else
                {
                    tranState.LblSpeed = " 正在连接…";
                }
                string lblState = "已上传：" + (offset * 100.0 / length).ToString("F2") + "%";
                tranState.LblState = lblState;
                string lblSize = (offset / 1048576.0).ToString("F2") + "M/" + (fileLength / 1048576.0).ToString("F2") + "M";
                tranState.LblSize= lblSize;
                Application.DoEvents();
                if (Value > count || count==100)
                {
                    count = Value;
                    form1.Invoke(upLoadDelgate, tranState);
                }
               
                size = binaryReader.Read(bArr, 0, bufferLength);
            }
                fs.Close();
            postStream.Write(endBoundaryBytes, 0, endBoundaryBytes.Length);
            postStream.Close();
            HttpWebResponse response =request.GetResponse() as HttpWebResponse;
            Stream instream = response.GetResponseStream();
            StreamReader sr = new StreamReader(instream, Encoding.UTF8);
            string content = sr.ReadToEnd();
            Console.WriteLine(" 上传完成…");
            return content;
        }