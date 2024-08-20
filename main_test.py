import unittest
from unittest.mock import patch, MagicMock
import main
import tkinter as tk


class TestMainApplication(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.root.geometry("400x800")

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def setUp(self):
        self.app = main

        self.mock_file_dialog = patch('main.filedialog.askopenfilename').start()

        self.mock_messagebox = patch('main.messagebox.showerror').start()
        self.mock_messagebox_info = patch('main.messagebox.showinfo').start()

    def tearDown(self):
        patch.stopall()

    def test_upload_action_valid_file(self):
        self.mock_file_dialog.return_value = "/path/to/file.xml"
        self.app.UploadAction()
        self.assertEqual(self.app.fileName, "file.xml")
        self.assertTrue(self.app.labelSelectedFile.cget("text"), "file.xml")

    def test_upload_second_file_action_valid_file(self):
        self.mock_file_dialog.return_value = "/path/to/file.dot"
        self.app.UploadSecondFileAction()
        self.assertEqual(self.app.secondFileName, "file.dot")
        self.assertTrue(self.app.labelSecondSelectedFile.cget("text"), "file.dot")

    def test_clear_file(self):
        self.app.fileName = "file.xml"
        self.app.clear_file()
        self.assertEqual(self.app.fileName, "")
        self.assertEqual(self.app.labelSelectedFile.cget("text"), "")

    def test_clear_second_file(self):
        self.app.secondFileName = "file.dot"
        self.app.clear_second_file()
        self.assertEqual(self.app.secondFileName, "")
        self.assertEqual(self.app.labelSecondSelectedFile.cget("text"), "")

    def test_check_fields_enable_run(self):
        self.app.fileName = "file.xml"
        self.app.secondFileName = "file.dot"
        self.app.check_fields()
        self.assertTrue(self.app.radio_r.cget("state") == tk.NORMAL)
        self.assertTrue(self.app.radio_t.cget("state") == tk.NORMAL)
        self.assertTrue(self.app.combobox.cget("state") == tk.NORMAL)
        self.assertTrue(self.app.runButton.cget("state") == tk.NORMAL)

    def test_check_fields_disable_run(self):
        # Test disabling fields when files are not selected
        self.app.fileName = ""
        self.app.secondFileName = ""
        self.app.check_fields()
        self.assertTrue(self.app.radio_r.cget("state") == tk.DISABLED)
        self.assertTrue(self.app.radio_t.cget("state") == tk.DISABLED)
        self.assertTrue(self.app.combobox.cget("state") == tk.DISABLED)
        self.assertTrue(self.app.runButton.cget("state") == tk.DISABLED)

    def test_run_action_no_files(self):
        self.app.fileName = ""
        self.app.secondFileName = ""
        self.app.run_action()
        self.mock_messagebox.assert_called_with("Lütfen tüm dosyaları seçin.")

    def test_run_action_invalid_combobox_value(self):
        self.app.fileName = "file.xml"
        self.app.secondFileName = "file.dot"
        self.app.combobox.set("100")
        self.app.run_action()
        self.mock_messagebox.assert_called_with("Lütfen geçerli bir sayı girin!")

    def test_run_action_valid(self):
        self.app.fileName = "file.xml"
        self.app.secondFileName = "file.dot"
        self.app.radio_var.set(0)
        self.app.combobox.set("10")
        with patch('main.print') as mock_print:
            self.app.run_action()
            mock_print.assert_called_with("file.xml", "file.dot", 0, 10)
            self.mock_messagebox_info.assert_called_with("Başarılı", "Veriler Başarıyla Yazdırıldı.")

    def test_save_data(self):
        commands = self.app.save_data("platform.xml", "log.dot", 0, 10)
        expected_commands = [
            "EvaluatorM.LoadPlatform('platform.xml')",
            "EvaluatorM.LoadTestLog('log.dot')",
            "EventM.CreateEvent('Ubas mux message', 'UBAS', 'MuxMessageContract => 0', QUERRYTYPE.QUERY_IS_BIGGER, '0', '0', '10', '')"
        ]
        self.assertEqual(commands, expected_commands)


if __name__ == '__main__':
    unittest.main()
