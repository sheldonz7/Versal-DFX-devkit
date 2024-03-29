from kernels.dummy_kernel import DummyKernel
import pdb
import subprocess
import time

class hash_kernel(DummyKernel):
    def __init__(self, dev, base_addr):
        super().__init__(dev, base_addr)
        # Register Offsets
        self.input_addr_offset_0 = 0x10
        self.input_addr_offset_1 = 0x14
        self.output_addr_offset_0 = 0x1c
        self.output_addr_offset_1 = 0x20
        self.batch_size_offset = 0x28
        self.ctrl_offset = 0x00

    def set_input_offset(self, offset): 
        lsb = offset & 0xFFFF_FFFF
        msb = offset >> 32
        self.dev.dma_write(self.base_addr + self.input_addr_offset_0, lsb.to_bytes(4, "little"))
        self.dev.dma_write(self.base_addr + self.input_addr_offset_1, msb.to_bytes(4, "little"))

    def set_output_offset(self, offset):
        lsb = offset & 0xFFFF_FFFF
        msb = offset >> 32
        self.dev.dma_write(self.base_addr + self.output_addr_offset_0, lsb.to_bytes(4, "little"))
        self.dev.dma_write(self.base_addr + self.output_addr_offset_1, msb.to_bytes(4, "little"))

    def set_batch_size(self, size):
        self.dev.dma_write(self.base_addr + self.batch_size_offset, size.to_bytes(4, "little"))

    
    def set_start(self):
        self.dev.dma_write(self.base_addr + self.ctrl_offset, int(0x1).to_bytes(1, "little"))

    def test(self):
        print(self.base_addr + self.ctrl_offset)
        return self.dev.dma_read(self.base_addr + self.ctrl_offset, 1)


    def get_axi_control(self):
        return int.from_bytes(self.dev.dma_read(self.base_addr + self.ctrl_offset, 4), 'little')

    def get_done(self):
        #breakpoint()
        reg = int.from_bytes(self.dev.dma_read(self.base_addr + self.ctrl_offset, 4), 'little')
        print(bin(reg))
        return reg & 0x2 == 0x2

    def wait_on_done(self):
        while not self.get_done():
            time.sleep(0.1)