from barktools.base_utils import RingBuffer

class TestRingBuffer:
    
    def test_1(self):
        buffer_size = 3
        ring_buffer = RingBuffer(buffer_size=buffer_size)
        items_to_put = [0,1,2,3,4,5,6,7,8,9]
        for item in items_to_put:
            ring_buffer.put(item)
        assert ring_buffer.items() == [9,7,8]
        assert ring_buffer.n_last(2) == [8,9]

    def test_2(self):
        buffer_size = 1
        ring_buffer = RingBuffer(buffer_size=buffer_size)
        for item in [1,2,3,4]:
            ring_buffer.put(item)
        assert ring_buffer.last() == 4  