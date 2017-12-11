using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Net;
using System.Windows.Controls;
using System.IO;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.IO.Compression;
using System.Windows.Media.Animation;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.ComponentModel;

namespace WpfApp1
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {

        private String status
        {
            set { statusLabel.Content = "Staða: " + value; }
            get { return statusLabel.Content.ToString().Substring(8); }
        }

        public MainWindow()
        {
            InitializeComponent();
        }

        private void installButtonClick(object sender, RoutedEventArgs e)
        {
            status = "Hleð niður (0%)";
            tranformToInstallMode(() => {
                Directory.CreateDirectory(@"c:\Program Files\GH Bílaleiga");

                WebClient webClient = new WebClient();
                webClient.DownloadProgressChanged += new DownloadProgressChangedEventHandler(downloadProgressChanged);
                webClient.DownloadFileCompleted += new AsyncCompletedEventHandler(downloadCompleted);
                webClient.DownloadFileAsync(new Uri("http://leiga.fisedush.com/api/download/desktopClient"), @"c:\Program Files\GH Bílaleiga\Desktop.zip");
            });
        }

        private void downloadProgressChanged(object sender, DownloadProgressChangedEventArgs e)
        {
            progressBar.Value = e.ProgressPercentage;
            status = $"Hleð niður ({e.ProgressPercentage}%)";
        }

        private void downloadCompleted(object sender, AsyncCompletedEventArgs e)
        {
            progressBar.Value = 0;
            status = $"Set upp (0%)";

            if (File.Exists(@"c:\Program Files\GH Bílaleiga\main.py"))
            {
                File.Delete(@"c:\Program Files\GH Bílaleiga\main.py");
            }
            if (File.Exists(@"c:\Program Files\GH Bílaleiga\loginwindow.ui"))
            {
                File.Delete(@"c:\Program Files\GH Bílaleiga\loginwindow.ui");
            }
            if (File.Exists(@"c:\Program Files\GH Bílaleiga\datepicker.ui"))
            {
                File.Delete(@"c:\Program Files\GH Bílaleiga\datepicker.ui");
            }
            if (File.Exists(@"c:\Program Files\GH Bílaleiga\mainwindow.ui"))
            {
                File.Delete(@"c:\Program Files\GH Bílaleiga\mainwindow.ui");
            }
            if (File.Exists(@"c:\Program Files\GH Bílaleiga\datepicker.py"))
            {
                File.Delete(@"c:\Program Files\GH Bílaleiga\datepicker.py");
            }
            if (File.Exists(@"c:\Program Files\GH Bílaleiga\loginData.json"))
            {
                File.Delete(@"c:\Program Files\GH Bílaleiga\loginData.json");
            }
            if (File.Exists(@"c:\Program Files\GH Bílaleiga\savedatamanager.py"))
            {
                File.Delete(@"c:\Program Files\GH Bílaleiga\savedatamanager.py");
            }

            ZipFile.ExtractToDirectory(@"c:\Program Files\GH Bílaleiga\Desktop.zip", @"c:\Program Files\GH Bílaleiga\");
            if (File.Exists(@"c:\Program Files\GH Bílaleiga\Desktop.zip"))
            {
                File.Delete(@"c:\Program Files\GH Bílaleiga\Desktop.zip");
            }

            progressBar.Value = 50;
            status = $"Set upp (50%)";

            var desktopDir = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile) + @"\Desktop";
            using (StreamWriter sw = File.CreateText(desktopDir + @"\bilaleiga.bat"))
            {
                sw.WriteLine(@"python C:\Program Files\GH Bílaleiga\main.py");
            }

            progressBar.Value = 100;
            status = $"Uppsetning tókst.  Opnaðu bilaleiga.bat á desktopinu";
        }

        private void tranformToInstallMode(Action onComplete)
        {
            animateOut(installButton, (control) => {
                installButton.Visibility = Visibility.Hidden;

                statusLabel.Visibility = Visibility.Visible;
                progressBar.Visibility = Visibility.Visible;
                animateIn(statusLabel, doNothingOnComplete);
                animateIn(progressBar, (control2) => {
                    onComplete();
                });
            });
        }

        private void doNothingOnComplete(Control control)
        {
            return;
        }

        private void animateIn(Control control, Action<Control> onComplete, int tranlateYValue = -30)
        {
            // TranslateY
            DoubleAnimation translateAnimation = new DoubleAnimation();
            translateAnimation.From = tranlateYValue;
            translateAnimation.To = 0;
            translateAnimation.Duration = new Duration(TimeSpan.FromSeconds(0.25));
            TranslateTransform translate = new TranslateTransform();
            control.RenderTransform = translate;
            translate.BeginAnimation(TranslateTransform.YProperty, translateAnimation);

            // Opacity
            Storyboard storyboard = new Storyboard();
            DoubleAnimation opacityAnimation = new DoubleAnimation();
            opacityAnimation.Completed += (sender, eventArgs) =>
            {
                onComplete(control);
            };
            opacityAnimation.From = 0.0;
            opacityAnimation.To = 1.0;
            opacityAnimation.Duration = new Duration(TimeSpan.FromSeconds(0.25));
            Storyboard.SetTarget(opacityAnimation, control);
            Storyboard.SetTargetName(opacityAnimation, control.Name);
            Storyboard.SetTargetProperty(opacityAnimation, new PropertyPath(Control.OpacityProperty));
            storyboard.Children.Add(opacityAnimation);
            storyboard.Begin(this);
        }

        private void animateOut(Control control, Action<Control> onComplete, int tranlateYValue = 30)
        {
            // TranslateX
            DoubleAnimation translateAnimation = new DoubleAnimation();
            translateAnimation.From = 0;
            translateAnimation.To = tranlateYValue;
            translateAnimation.Duration = new Duration(TimeSpan.FromSeconds(0.25));
            TranslateTransform translate = new TranslateTransform();
            control.RenderTransform = translate;
            translate.BeginAnimation(TranslateTransform.YProperty, translateAnimation);

            // Opacity
            Storyboard storyboard = new Storyboard();
            DoubleAnimation opacityAnimation = new DoubleAnimation();
            opacityAnimation.Completed += (sender, eventArgs) =>
            {
                onComplete(control);
            };
            opacityAnimation.From = 1.0;
            opacityAnimation.To = 0.0;
            opacityAnimation.Duration = new Duration(TimeSpan.FromSeconds(0.25));
            Storyboard.SetTargetName(opacityAnimation, control.Name);
            Storyboard.SetTargetProperty(opacityAnimation, new PropertyPath(Control.OpacityProperty));
            storyboard.Children.Add(opacityAnimation);
            storyboard.Begin(this);
        }
    }
}
