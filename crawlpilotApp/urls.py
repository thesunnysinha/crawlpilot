from django.urls import path
from .views import CrawlURLView, AsyncBulkCrawlView, CrawlStatusView, ReportView, VectorSimilarityView

urlpatterns = [
    path('crawl-url/', CrawlURLView.as_view(), name='crawl_url'),
    path('async-bulk-crawl/', AsyncBulkCrawlView.as_view(), name='async_bulk_crawl'),
    path('crawl-status/', CrawlStatusView.as_view(), name='crawl_status'),
    path('report/', ReportView.as_view(), name='report'),
    path('vector-similarity/', VectorSimilarityView.as_view(), name='vector_similarity'),
]
