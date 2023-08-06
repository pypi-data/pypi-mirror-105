#include "py14/runtime/builtins.h"
#include "py14/runtime/sys.h"
#include <algorithm>
#include <cassert>
#include <iostream>
#include <map>
#include <set>
int code_0 = 0;
int code_1 = 1;
std::string code_a = std::string{"a"};
std::string code_b = std::string{"b"};
std::set<std::string> l_b = std::set<std::string>{code_a};
std::map<std::string, int> l_c = std::map<std::string, int>{{code_b, code_0}};
int main(int argc, char **argv) {
  py14::sys::argv = std::vector<std::string>(argv, argv + argc);
  assert((std::find(l_b.begin(), l_b.end(), std::string{"a"}) != l_b.end()));
  std::cout << std::string{"OK"};
  std::cout << std::endl;
}
