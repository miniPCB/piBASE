using System;
using System.Drawing;
using System.IO.Ports;
using System.Windows.Forms;

namespace MyWindowsApp
{
    public partial class Form1 : Form
    {
        private TabControl tabControl;
        private TabPage terminalTab;
        private TabPage serialSettingsTab;
        private TabPage motorControlTab; // New Tab for Motor Jog Controls
        private TextBox terminalTextBox;
        private ComboBox portNameComboBox;
        private ComboBox baudRateComboBox;
        private ComboBox dataBitsComboBox;
        private ComboBox parityComboBox;
        private ComboBox stopBitsComboBox;
        private ComboBox flowControlComboBox;
        private Button connectButton;
        private Button cancelButton;
        private Button upButton; // New buttons for motor control
        private Button downButton;
        private Button leftButton;
        private Button rightButton;

        public Form1()
        {
            InitializeComponent();
            InitializeTabs();
        }

        private void InitializeTabs()
        {
            // Set form properties
            this.Text = "Serial Terminal with Motor Control";
            this.Size = new Size(800, 600);

            // Initialize TabControl
            tabControl = new TabControl();
            tabControl.Dock = DockStyle.Fill;

            // Initialize Terminal Tab
            terminalTab = new TabPage("Terminal");
            InitializeTerminalTab();

            // Initialize Serial Settings Tab
            serialSettingsTab = new TabPage("Serial Port Settings");
            InitializeSerialSettingsTab();

            // Initialize Motor Control Tab
            motorControlTab = new TabPage("Motor Control");
            InitializeMotorControlTab();

            // Add tabs to TabControl
            tabControl.TabPages.Add(terminalTab);
            tabControl.TabPages.Add(serialSettingsTab);
            tabControl.TabPages.Add(motorControlTab);

            // Add TabControl to the form
            this.Controls.Add(tabControl);
        }

        private void InitializeTerminalTab()
        {
            // Initialize and customize the TextBox for terminal
            terminalTextBox = new TextBox();
            terminalTextBox.Multiline = true;
            terminalTextBox.Dock = DockStyle.Fill;
            terminalTextBox.BackColor = Color.Black;
            terminalTextBox.ForeColor = Color.White;
            terminalTextBox.Font = new Font("Consolas", 12, FontStyle.Regular);
            terminalTextBox.BorderStyle = BorderStyle.None;
            terminalTextBox.ScrollBars = ScrollBars.Vertical;
            terminalTextBox.AcceptsReturn = true;
            terminalTextBox.AcceptsTab = true;

            // Add the TextBox to the terminalTab
            terminalTab.Controls.Add(terminalTextBox);
        }

        private void InitializeSerialSettingsTab()
        {
            // Initialize Labels and ComboBoxes for each setting
            Label portNameLabel = new Label() { Text = "Port Name:", Location = new Point(20, 20) };
            portNameComboBox = new ComboBox() { Location = new Point(150, 20), Width = 200 };
            portNameComboBox.Items.AddRange(SerialPort.GetPortNames());

            Label baudRateLabel = new Label() { Text = "Baud Rate:", Location = new Point(20, 60) };
            baudRateComboBox = new ComboBox() { Location = new Point(150, 60), Width = 200 };
            baudRateComboBox.Items.AddRange(new string[] { "9600", "19200", "38400", "57600", "115200" });

            Label dataBitsLabel = new Label() { Text = "Data Bits:", Location = new Point(20, 100) };
            dataBitsComboBox = new ComboBox() { Location = new Point(150, 100), Width = 200 };
            dataBitsComboBox.Items.AddRange(new string[] { "5", "6", "7", "8" });

            Label parityLabel = new Label() { Text = "Parity:", Location = new Point(20, 140) };
            parityComboBox = new ComboBox() { Location = new Point(150, 140), Width = 200 };
            parityComboBox.Items.AddRange(Enum.GetNames(typeof(Parity)));

            Label stopBitsLabel = new Label() { Text = "Stop Bits:", Location = new Point(20, 180) };
            stopBitsComboBox = new ComboBox() { Location = new Point(150, 180), Width = 200 };
            stopBitsComboBox.Items.AddRange(Enum.GetNames(typeof(StopBits)));

            Label flowControlLabel = new Label() { Text = "Flow Control:", Location = new Point(20, 220) };
            flowControlComboBox = new ComboBox() { Location = new Point(150, 220), Width = 200 };
            flowControlComboBox.Items.AddRange(new string[] { "None", "RTS/CTS", "XON/XOFF" });

            // Initialize Connect and Cancel Buttons
            connectButton = new Button() { Text = "Connect", Location = new Point(150, 260), Size = new Size(100, 50) };
            connectButton.Click += ConnectButton_Click;

            cancelButton = new Button() { Text = "Cancel", Location = new Point(260, 260), Size = new Size(100, 50) };
            cancelButton.Click += CancelButton_Click;

            // Add controls to the serialSettingsTab
            serialSettingsTab.Controls.Add(portNameLabel);
            serialSettingsTab.Controls.Add(portNameComboBox);
            serialSettingsTab.Controls.Add(baudRateLabel);
            serialSettingsTab.Controls.Add(baudRateComboBox);
            serialSettingsTab.Controls.Add(dataBitsLabel);
            serialSettingsTab.Controls.Add(dataBitsComboBox);
            serialSettingsTab.Controls.Add(parityLabel);
            serialSettingsTab.Controls.Add(parityComboBox);
            serialSettingsTab.Controls.Add(stopBitsLabel);
            serialSettingsTab.Controls.Add(stopBitsComboBox);
            serialSettingsTab.Controls.Add(flowControlLabel);
            serialSettingsTab.Controls.Add(flowControlComboBox);
            serialSettingsTab.Controls.Add(connectButton);
            serialSettingsTab.Controls.Add(cancelButton);
        }

        private void InitializeMotorControlTab()
        {
            // Initialize motor control buttons
            upButton = new Button() { Text = "Up", Location = new Point(100, 50), Size = new Size(100, 50) };
            upButton.Click += UpButton_Click;

            downButton = new Button() { Text = "Down", Location = new Point(100, 150), Size = new Size(100, 50) };
            downButton.Click += DownButton_Click;

            leftButton = new Button() { Text = "Left", Location = new Point(20, 100), Size = new Size(100, 50) };
            leftButton.Click += LeftButton_Click;

            rightButton = new Button() { Text = "Right", Location = new Point(180, 100), Size = new Size(100, 50) };
            rightButton.Click += RightButton_Click;

            // Add buttons to the motorControlTab
            motorControlTab.Controls.Add(upButton);
            motorControlTab.Controls.Add(downButton);
            motorControlTab.Controls.Add(leftButton);
            motorControlTab.Controls.Add(rightButton);
        }

        // Event handlers for motor control buttons
        private void UpButton_Click(object sender, EventArgs e)
        {
            // Code to jog motor up
            MessageBox.Show("Jogging Up");
        }

        private void DownButton_Click(object sender, EventArgs e)
        {
            // Code to jog motor down
            MessageBox.Show("Jogging Down");
        }

        private void LeftButton_Click(object sender, EventArgs e)
        {
            // Code to jog motor left
            MessageBox.Show("Jogging Left");
        }

        private void RightButton_Click(object sender, EventArgs e)
        {
            // Code to jog motor right
            MessageBox.Show("Jogging Right");
        }

        private void ConnectButton_Click(object sender, EventArgs e)
        {
            // Handle the connection logic here
            try
            {
                SerialPort serialPort = new SerialPort()
                {
                    PortName = portNameComboBox.SelectedItem.ToString(),
                    BaudRate = int.Parse(baudRateComboBox.SelectedItem.ToString()),
                    DataBits = int.Parse(dataBitsComboBox.SelectedItem.ToString()),
                    Parity = (Parity)Enum.Parse(typeof(Parity), parityComboBox.SelectedItem.ToString()),
                    StopBits = (StopBits)Enum.Parse(typeof(StopBits), stopBitsComboBox.SelectedItem.ToString()),
                    Handshake = flowControlComboBox.SelectedItem.ToString() == "None" ? Handshake.None :
                                flowControlComboBox.SelectedItem.ToString() == "RTS/CTS" ? Handshake.RequestToSend :
                                Handshake.XOnXOff
                };

                serialPort.Open();
                MessageBox.Show("Connected successfully!", "Connection Status", MessageBoxButtons.OK, MessageBoxIcon.Information);
                // You can now use serialPort to read/write data
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Failed to connect: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void CancelButton_Click(object sender, EventArgs e)
        {
            this.Close();
        }
    }
}
