from pathlib import Path
from qibolab.instruments.dummy import DummyInstrument
from qibolab.platform import Platform
from qibolab.channels import Channel, ChannelMap
from qibolab.serialize import load_runcard, load_qubits


FOLDER = Path(__file__).parent

def create():
    instrument = DummyInstrument("myinstr", "0.0.0.0:0")

    channels = ChannelMap()
    channels |= Channel(
        "readout", 
        port=instrument.ports("o1")
    )
    channels |= Channel(
        "feedback", 
        port=instrument.ports("i1", output=False)
    )
    channels |= Channel(
        "drive", 
        port=instrument.ports("o2")
    )
    
    
    runcard = load_runcard(FOLDER)
    qubits, couplers, pairs = load_qubits(runcard)

    qubits[0].readout = channels["readout"]
    qubits[0].feedback = channels["feedback"]
    qubits[0].drive = channels["drive"]

    return Platform(
        "myplatform", 
        qubits, 
        pairs, 
        instruments={instrument.name: instrument}, 
    )
