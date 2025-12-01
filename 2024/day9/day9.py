from dataclasses import dataclass


@dataclass
class Block:
    offset: int
    length: int
    file_index: str

    @property
    def end(self) -> int:
        return self.offset + self.length


class FileSystem:
    def __init__(self, disk_map: str):
        self.blocks = []
        self.free_blocks = []
        self.size = 0
        offset = 0
        for index, block_length in enumerate(disk_map):
            block_length = int(block_length)
            if block_length == 0:
                continue
            content = None if index % 2 != 0 else str(index // 2)
            if content:
                self.blocks.append(Block(offset, block_length, content))
            else:
                self.free_blocks.append(Block(offset, block_length, '.'))
            offset += block_length
        self.size = offset

    def verify(self):
        # verify order and lengths
        for b1, b2 in zip(self.blocks[:-1], self.blocks[1:]):
            if b1.offset >= b2.offset:
                print(f'ERROR: offset of block n is not smaller than offset of block n+1: {b1}, {b2}')
                return False
            if b1.offset + b1.length > b2.offset:
                print(f'ERROR: offset + length of block n is larger than offset of block n+1: {b1} {b2}')
                return False
        return True

    def compact(self, print_steps: bool = False):
        offset = 0
        next_block = 0
        while next_block != len(self.blocks):
            next_block_offset = self.blocks[next_block].offset
            if offset == next_block_offset:
                offset += self.blocks[next_block].length
                next_block += 1
                continue
            size_required = next_block_offset - offset
            last_block = self.blocks[-1]
            if size_required < last_block.length and next_block != len(self.blocks) - 1:
                # cut off part of the last block, place it here
                # !addition: except if the last block is the next block, in that case move entire block
                last_block.length -= size_required
                new_block = Block(offset, size_required, last_block.file_index)
            else:
                # place last block here
                last_block.offset = offset
                self.blocks.remove(last_block)
                new_block = last_block
            self.blocks.insert(next_block, new_block)
            offset += new_block.length
            next_block += 1
            if print_steps:
                print(self)
            continue
        self.recalc_free_blocks()

    def recalc_free_blocks(self):
        self.free_blocks = []
        first_block = self.blocks[0]
        if first_block.offset != 0:
            self.free_blocks.append(Block(0, first_block.offset, '.'))
        for b1, b2 in zip(self.blocks[:-1], self.blocks[1:]):
            if b1.end < b2.offset:
                self.free_blocks.append(Block(b1.end, b2.offset - b1.end, '.'))
        last_block = self.blocks[-1]
        if last_block.end < self.size:
            self.free_blocks.append(Block(last_block.end, self.size - last_block.end, '.'))

    def compact_without_fragmentation(self,print_steps: bool = False):
        for file in reversed(self.blocks):
            for free_block_index, free_block in enumerate(self.free_blocks):
                if free_block.offset > file.offset:
                    break
                if free_block.length < file.length:
                    continue
                # we can move file forward!
                file.offset = free_block.offset
                if free_block.length == file.length:
                    self.free_blocks.remove(free_block)
                else:
                    free_block.offset += file.length
                    free_block.length -= file.length
                if print_steps:
                    self.blocks.sort(key=lambda b: b.offset)
                    print(self)
                break
        if not print_steps:
            self.blocks.sort(key=lambda b: b.offset)

    def checksum(self) -> int:
        checksum = 0
        for block in self.blocks:
            for i in range(block.length):
                checksum += (block.offset + i) * int(block.file_index)
        return checksum

    def __str__(self):
        if not self.verify():
            return ''
        index = 0
        string = ''
        for block in self.blocks:
            if index < block.offset:
                string += '.' * (block.offset - index)
                index = block.offset
            string += f'{block.file_index}' * block.length
            index += block.length
        if index != self.size:
            string += '.' * (self.size - index)
        return string


if __name__ == '__main__':
    test_input = '2333133121414131402'
    with open('input.txt', 'r') as file:
        input = file.read().strip()

    print('part 1')
    fs = FileSystem(input)
    fs.compact(print_steps=False)
    print(fs.checksum())
    print('part 2')
    fs = FileSystem(input)
    fs.compact_without_fragmentation(print_steps=False)
    print(fs.checksum())
