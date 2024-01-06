#!/usr/bin/python3

#crappy implementation of section 3.3 of https://cseweb.ucsd.edu/~tullsen/halfandhalf.pdf

def gen_code(n,osx,o,ll):
    l = ''
    takenfiller = True
    if osx:
        l = '_'
        o.write('.globl _foo%d\n' % n)
    else:
        o.write('.global foo%d\n' % n)

    if takenfiller:
        bt = 'z'
    else:
        bt = 'nz'
        
    o.write('%sfoo%d:\n' % (l, n))
    o.write('.L%d:\n' % ll)
    ss = ll
    ll = ll + 1

    o.write('slli	a4,a0,13\n')
    o.write('xor	a4,a4,a0\n')
    o.write('srli	a5,a4,17\n')
    o.write('xor	a5,a5,a4\n')
    o.write('slli	a0,a5,5\n')
    o.write('andi	a4,a5,1\n')
    o.write('xor	a0,a0,a5\n')    

    o.write('beq	a4, zero, .L%d\n' % ll)
    o.write('nop\n')
    o.write('.L%d:\n' % ll)
    ll = ll + 1
    for i in range(0, n):
        o.write('j .LL%d\n' % (ll))
        o.write('.LL%d:\n' % ll)
        ll = ll + 1
    o.write('beq	a4, zero, .L%d\n' % ll)        
    o.write('nop\n')
    o.write('.L%d:\n' % ll)
    ll = ll + 1
    o.write('addi	a1,a1,-1\n')    
    o.write('bne a1,zero,.L%d\n' % ss)
    o.write('ret\n')
    return ll


if __name__ == '__main__':
    o = open('functions.s', 'w')
    ll = 0
    n = 64
    for i in range(1, n):
        ll = gen_code(i, False, o, ll)
    o.close()
    o = open('header.h', 'w')
    o.write('#include <stdint.h>\n')
    for i in range(1, n):
        o.write('uint32_t foo%d(uint32_t x, uint32_t c);\n' % i)

    o.write('uint32_t (*funcs[]) (uint32_t, uint32_t) = {\n')
    for i in range(1, n):
        o.write('foo%d,\n' % i)
    
    o.write('};\n')
        
    o.close()
        
