import sys
import threading

# import msg
import sim
import spu

if __name__ == '__main__':

    app = spu.QApplication(sys.argv)
    ex = spu.Serialwindow()

    spu_t = threading.Thread(target=ex.show)
    sim_t = threading.Thread(target=sim.Sim)
    spu_t.start()
    sim_t.start()
    
    sys.exit(app.exec_())
    