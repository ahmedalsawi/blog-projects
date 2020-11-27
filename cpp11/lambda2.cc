#include <iostream>

using namespace std;

auto lamda1 = [](auto a) { cout << a << endl; };

int main()
{
    lamda1(1);
}