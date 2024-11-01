#pragma once

#include "CMealy.h"
#include "CMoore.h"
#include <algorithm>
#include <string>

class CMinimizer
{
    public:
        static void MealyMinimizer(CMealy &mealy);
        static void MooreMinimizer(CMoore &moore);
};
