#pragma once

#include <vector>

#include <viewshedutils.h>
#include <visibilityalgorithms.h>

using viewshed::AbstractViewshedAlgorithm;

using VisibilityAlgoritms = std::vector<std::shared_ptr<AbstractViewshedAlgorithm>>;

class VisibilityAlgs
{
  public:
    VisibilityAlgs( bool singleAlgorithm, double noData = std::numeric_limits<double>::quiet_NaN() );

    size_t size();

    std::shared_ptr<VisibilityAlgoritms> get();

  private:
    std::shared_ptr<VisibilityAlgoritms> mAlgs = std::make_shared<VisibilityAlgoritms>();
};