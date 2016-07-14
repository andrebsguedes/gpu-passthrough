#include <tuple>
#include <iostream>
#include <chrono>
#include <thread>

std::tuple<int, bool, float> foo()
{
	return std::make_tuple(128, true, 1.5f);
}
int main(int argc, char* argv[])
{
	std::tuple<int, bool, float> result = foo();
	int value = std::get<0>(result);
	int obj1;
	bool obj2;
	float obj3;
    using namespace std::chrono_literals;
	std::tie(obj1, obj2, obj3) = foo();
    std::cout << "ARGS" << std::endl << argv[1];
    std::this_thread::sleep_for(2s);
    std::cout << "while" << std::endl;
}
