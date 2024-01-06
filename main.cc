#include <cstdlib>
#include <cstdio>
#include <iostream>

extern "C" {
#include "header.h"
};

static const size_t n_funcs = sizeof(funcs)/sizeof(funcs[0]);
static const uint32_t n_iters = 1U<<16;

void *__dso_handle = nullptr;



#define read_csr_safe(reg) (\
    { uint32_t __tmp;			       \
      asm volatile ("csrr %0, " #reg : "=r"(__tmp));   \
      __tmp; }\
    )


int main() {

  for(size_t i = 0; i < n_funcs; i++) {
    uint32_t m0 = read_csr_safe(hpmcounter4);
    funcs[i](1, n_iters);
    m0 = read_csr_safe(hpmcounter4) - m0;
    std::cout << i << "," << m0 << "\n";
    // c1.missed_branches -= c0.missed_branches;
    // c1.branches -= c0.branches;

    // //subtract out dummy branches and loop backedge
    // c1.branches -= n_iters * (i+2); 

    // double r = static_cast<double>(c1.missed_branches) / c1.branches;
    // std::cout << i << "," << r << "\n";
    
  }
  
  return 0;
}
