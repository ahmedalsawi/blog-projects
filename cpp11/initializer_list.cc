#include <initializer_list>
#include <iostream>
using namespace std;

class cls
{
public:
    void func(std::initializer_list<int> ins)
    {
        for (auto in : ins)
            cout << in << endl;
    }
};

int main()
{
    cls c;
    c.func({1, 2, 3});
    return 0;
}