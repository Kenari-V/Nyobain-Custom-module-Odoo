from email.policy import default
from io import BytesIO
from pyclbr import Class
from pyexpat import model
import string
import random
from unicodedata import name
import qrcode
import base64

from attr import field
from soupsieve import select
from odoo import fields, models, api

class PengunjungProfile(models.Model):
   _name = "pengunjung.profile"
   _rec_name = "nama"

   noVisit = fields.Char(string="No Visitor")
   nama = fields.Char(string="Nama")
   email = fields.Char(string="Email")
   phone = fields.Char(string="No Telepon")
   tanggaldatang = fields.Datetime("Tanggal Datang")
   foto_Ktp = fields.Image(string="Foto Identitas", max_width=100,
                          max_height=60, verify_resolution=True)
   tujuan_id = fields.Many2one('karyawan.profile', string='Tujuan')
   keperluan = fields.Char('Keperluan')
   ruangan_id = fields.Many2one('ruangan.profile', string='Ruangan')
   durasi = fields.Selection([
      ('1j', '1 Jam'),
      ('2j', '2 Jam'),
      ('3j', '3 Jam'),
      ('4j', '4 Jam'),
      ('5j', '5 Jam'),
      ('6j', '6 Jam'),
      ('7j', '7 Jam'),
      ('8j', '8 Jam'),
      ('9j', '9 Jam'),
      ('10j', '10 Jam')
    ], string='Durasi')
   keterangan = fields.Text('Keterangan')

   state = fields.Selection([
      ('Registrasi', 'Registrasi'),
      ('Konfirmasi', 'Konfirmasi'),
      ('Progress', 'Progress'),
      ('Selesai', 'Selesai'),
      ('Cancel', 'Cancel')
   ], default='Registrasi',string='status')

   # qr_code = fields.Binary('QR Code', attachment=True)
   
   # api.onchange('default_code')
   # def generate_qr_code(self):
   #    qr = qr.QRCode(
   #       version=1,
   #       error_correction=qr.constants.ERROR_CORRECT_L,
   #       box_size=10,
   #       border=4,
   #    )

   #    qr.add_data(self.default_code)
   #    qr.make(fit=True)
   #    img = qr.make_image()
   #    temp = BytesIO()
   #    img.save(temp, format="PNG")
   #    qr_image = base64.b64encode(temp.getvalue())
   #    self.qr_code = qr_image

   def action_confirm (self):
      self.state = "Konfirmasi"

   def action_progress (self):
      self.state = "Progress"

   def action_selesai (self):
      self.state = "Selesai"
   
   def action_cancel (self):
      self.state = "Cancel"
   

   @api.model
   def create(self, vals):
      vals['noVisit'] = self.env['ir.sequence'].next_by_code('pengunjung.profile')
      return super(PengunjungProfile, self).create(vals)



class karyawan_profile(models.Model):
   _name = 'karyawan.profile'
   _description = 'karyawan_profile'
   _rec_name = "nama"
   
   nama = fields.Char('Nama')
   jenisKelamin = fields.Selection([
      ('L', 'Laki-Laki'),
      ('P', 'Perempuan')
   ], string='Jenis Kelamin')

   jabatan = fields.Char('Jabatan')
   departement = fields.Char('Departement')
   mengunjungi_ids = fields.One2many('pengunjung.profile','tujuan_id', string='Orang Yang Mengunjungi')



class ruangan_profile(models.Model):
   _name = 'ruangan.profile'
   _description = 'ruangan_profile'
   _rec_name = "ruangan"

   lantai = fields.Selection([
      ('L1', 'Lantai 1'),
      ('L2', 'Lantai 2'),
      ('L3', 'Lantai 3'),
      ('L4', 'Lantai 4'),
      ('L5', 'Lantai 5'),
      ('L6', 'Lantai 6'),
      ('L7', 'Lantai 7'),
      ('L8', 'Lantai 8')
   ], string='Lantai') 
   ruangan = fields.Char('Ruangan')

   def   name_get(self):
     pengunjung_list = []
     for pengunjung in self:
        print(self, pengunjung)
        name = pengunjung.ruangan
        if pengunjung.lantai:
           name += "({})".format(pengunjung.lantai)
           pengunjung_list.append((pengunjung.id, name))
     return pengunjung_list


# class qrcode(models.Model):
#    _inherit = "pengunjung.profile"

#    qr_code = fields.Binary('QR Code', attachment=True)
   
#    api.onchange('default_code')
#    def generate_qr_code(self):
#       qr = qr.QRCode(
#          version=1,
#          error_correction=qr.constants.ERROR_CORRECT_L,
#          box_size=10,
#          border=4,
#       )

#       qr.add_data(self.default_code)
#       qr.make(fit=True)
#       img = qr.make_image()
#       temp = BytesIO()
#       img.save(temp, format="PNG")
#       qr_image = base64.b64encode(temp.getvalue())
#       self.qr_code = qr_image 
class qr_code(models.Model):
   _inherit = 'pengunjung.profile'

   def _generate_qr(self):
      for rec in self:
         rec.qr_code = str(rec.id)
   
   def print_qrcode(self):
      return{
         'type': 'ir.actions.report',
         'report_name': 'latihan_custom_Module.reportQr_Code',
         'report_type': 'qweb-pdf'
      }

   qr_code = fields.Char(string="QR Code", compute=_generate_qr)

   








