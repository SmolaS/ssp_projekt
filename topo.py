from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import time

class PaperTopo(Topo):
    def build(self):
        # 1. Dodanie hostów
        ftp_srv = self.addHost('ftp_srv', ip='10.0.0.1/24')
        db_srv = self.addHost('db_srv', ip='10.0.0.2/24')
        ftp_usr = self.addHost('ftp_usr', ip='10.0.0.3/24')
        db_usr1 = self.addHost('db_usr1', ip='10.0.0.4/24')
        db_usr2 = self.addHost('db_usr2', ip='10.0.0.5/24')

        # 2. Dodanie przełączników
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')
        s8 = self.addSwitch('s8')

        # 3. Podłączenie hostów do przełączników
        self.addLink(ftp_srv, s5)
        self.addLink(db_srv, s4)
        self.addLink(ftp_usr, s3)
        self.addLink(db_usr1, s2)
        self.addLink(db_usr2, s1)

        # 4. Połączenia między przełącznikami
        # Waga 1 -> opóźnienie 10ms, pasmo 100 Mbps
        # Waga 2 -> opóźnienie 20ms, pasmo 50 Mbps

        # Linki o wadze 1 (pogrubione na schemacie)
        self.addLink(s5, s4, bw=100, delay='10ms')
        self.addLink(s5, s6, bw=100, delay='10ms')
        self.addLink(s3, s8, bw=100, delay='10ms')
        self.addLink(s3, s2, bw=100, delay='10ms')

        # Linki o wadze 2 (cieńsze na schemacie)
        self.addLink(s4, s3, bw=50, delay='20ms')
        self.addLink(s6, s8, bw=50, delay='20ms')
        self.addLink(s6, s7, bw=50, delay='20ms')
        self.addLink(s8, s7, bw=50, delay='20ms')
        self.addLink(s7, s1, bw=50, delay='20ms')
        self.addLink(s1, s2, bw=50, delay='20ms')

if __name__ == '__main__':
    setLogLevel('info')
    topo = PaperTopo()

    net = Mininet(topo=topo, controller=OVSController, link=TCLink)
    net.start()

    # Włączenie STP na każdym switchu
    print("*** Włączanie protokołu STP na przełącznikach...")
    for sw in net.switches:
        sw.cmd('ovs-vsctl set Bridge', sw.name, 'stp_enable=true')

    print("*** Czekam 30 sekund na zbieżność drzewa STP...")
    time.sleep(30)

    print("*** Sieć gotowa do testów!")
    CLI(net)
    net.stop()