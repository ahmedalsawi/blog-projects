#include <iostream>
using namespace std;

class parent
{
public:
    int x;
};

class child : public parent
{
public:
    int x;
    child(int x) { cout << x << endl; }
    child() = default;
};
int main()
{
    child c;
    return 0;
}