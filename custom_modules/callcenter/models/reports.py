from odoo import fields, models,api
import os
import psycopg2
import csv


class Reports(models.Model):

    _name = 'reports.reports'
    _rec_name = 'phone'


    name= fields.Char()
    phone = fields.Char()
    address = fields.Char()
    city= fields.Char()
    # qualification = fields.Char()
    qualification = fields.Selection([
        ('crm', 'CRM'),
        ('rappel', 'Rappel'),
        ('appel nauel', 'Appel manuel'),
        ('cb', 'CB')], default='crm', )


    @api.model
    def _cron_update(self):
        print('test')
        # Connect to database
        con = psycopg2.connect(database='odoodb', user='odoo16')
        cur = con.cursor()
        folder_path = "/home/raja/files_csv"
        # get files in directory
        files = os.listdir(folder_path)
        print(files)
        for filename in files :
            print(os.path.join(folder_path,filename))
            with open(os.path.join(folder_path,filename)) as f:
                re = csv.reader(f, delimiter=',')
                next(re)
                print(re)
                rows = []
                for row in re:
                    rows.append(row)
                    data = cur.execute(
                        "INSERT INTO reports_reports(name, phone, address, city,qualification) VALUES (%s, %s, %s, %s, 'crm')", row)
                    con.commit()

            os.remove(os.path.join(folder_path,filename))

















