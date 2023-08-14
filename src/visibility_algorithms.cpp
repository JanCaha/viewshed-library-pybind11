#include <cmath>
#include <limits>

#include <visibility_algorithms.h>

using viewshed::ViewshedUtils;

VisibilityAlgs::VisibilityAlgs( bool singleAlgorithm, double noData )
{
    if ( singleAlgorithm )
    {
        mAlgs->push_back( std::make_shared<viewshed::visibilityalgorithm::Boolean>() );
    }
    else
    {
        if ( std::isnan( noData ) )
        {
            mAlgs = ViewshedUtils::allAlgorithms();
        }
        else
        {
            mAlgs = ViewshedUtils::allAlgorithms( noData );
        }
    }
}

size_t VisibilityAlgs::size() { return mAlgs->size(); }

std::shared_ptr<VisibilityAlgoritms> VisibilityAlgs::get() { return mAlgs; }
