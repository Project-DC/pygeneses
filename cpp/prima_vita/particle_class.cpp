#include <cstdlib>
#include <iostream>

#include "global_constants.hpp"

class Particle {
private:
  int particleX, particleY;

public:
  Particle() {
    particleX = 10 + (rand() % static_cast<int>(SCREEN_WIDTH - 20 + 1));
    particleY = 10 + (rand() % static_cast<int>(SCREEN_HEIGHT - 20 + 1));
  }

  int get_particleX() {
    return particleX;
  }

  int get_particleY() {
    return particleY;
  }
};

int main() {
  Particle particle;
  std::cout << particle.get_particleX() << std::endl;
  std::cout << particle.get_particleY() << std::endl;
}
