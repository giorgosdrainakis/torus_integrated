import csv
import os

from torus_integrated import myglobal
class Torus_Matrix:
    def __init__(self):
        self.db = []
        self.load()

    def load(self):
        combined_name=os.path.join(myglobal.ROOT,myglobal.INTER_TRANSMISSION_INFO_FOLDER)
        combined_name = os.path.join(combined_name, myglobal.TORUS_FILE)
        with open(combined_name) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                new_rec=Torus_Record(row['rx'],row['tx'],row['out_dir'],row['in_dir'],row['lamda'])
                self.db.append(new_rec)

    def get_trx_info_from_tx_rx_id(self,tx_id,rx_id):
        for rec in self.db:
            if tx_id==rec.tx and rx_id==rec.rx:
                return rec.out_dir,rec.in_dir,rec.lamda

    def get_15_lamda_request_from_rx_list(self,rx_list,tx):
        ports=15
        while ports>0:
            potentials=[]
            for quatro in itertools.combinations(rx_list, ports):
                # check if 4 different ports with 4 different channels
                out=[]
                for rx in quatro:
                    for rec in self.db:
                        if rec.tx==tx and rec.rx==rx:
                            out.append(rec)
                out_lamdas=[]
                out_ports=[]
                for el in out:
                    out_lamdas.append(el.lamda)
                    out_ports.append(el.out_dir)
                out_lamdas=list(set(out_lamdas))
                out_ports=list(set(out_ports))
                if len(out_lamdas)==ports and len(out_ports)==ports:
                    potentials.append(out)
            if len(potentials)>0:
                random.shuffle(potentials)
                return potentials[0]
            ports=ports-1
        return []

class Torus_Record:
    def __init__(self, rx,tx,out_dir,in_dir,lamda):
        self.rx=int(rx)
        self.tx=int(tx)
        self.out_dir=str(out_dir)
        self.in_dir=str(in_dir)
        self.lamda=int(lamda)
        self.size=0

    def show(self):
        print('tx='+str(self.tx)+',outdir='+str(self.out_dir)+',rx='+str(self.rx)+',indir='+str(self.in_dir))