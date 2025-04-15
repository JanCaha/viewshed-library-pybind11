#include <cmath>
#include <limits>

#include <visibility_algorithms.h>

using viewshed::ViewshedUtils;

VisibilityAlgs::VisibilityAlgs( double noData )
{

    mAlgs->push_back( std::make_shared<viewshed::visibilityalgorithm::Boolean>() );

    if ( !std::isnan( noData ) )
    {
        mNoData = noData;
    }
}

size_t VisibilityAlgs::size() { return mAlgs->size(); }

std::shared_ptr<VisibilityAlgoritms> VisibilityAlgs::get() { return mAlgs; }

void VisibilityAlgs::addAll()
{
    if ( !std::isnan( mNoData ) )
    {
        mAlgs = ViewshedUtils::allAlgorithms();
    }
    else
    {
        mAlgs = ViewshedUtils::allAlgorithms( mNoData );
    }
}
