# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CrawledURL, CrawlingStatus
from .serializers import CrawledURLSerializer, CrawlingStatusSerializer
from .utils import scrape_page
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

class CrawlURLView(APIView):
    def post(self, request):
        url = request.data.get('url')
        if not url:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        title, summary, links = scrape_page(url)
        crawled_data = CrawledURL.objects.create(url=url, title=title, summary=summary, links=links)
        serializer = CrawledURLSerializer(crawled_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AsyncBulkCrawlView(APIView):
    def post(self, request):
        urls = request.data.get('urls')
        if not urls or not isinstance(urls, list):
            return Response({"error": "A list of URLs is required"}, status=status.HTTP_400_BAD_REQUEST)

        for url in urls:
            CrawlingStatus.objects.create(url=url, status='in progress')
            # Here you would enqueue a background task to process the URL
            # For now, we're just processing synchronously
            CrawlURLView.as_view()(request)

        return Response({"status": "success"}, status=status.HTTP_202_ACCEPTED)

class CrawlStatusView(APIView):
    def get(self, request):
        status_list = CrawlingStatus.objects.all()
        serializer = CrawlingStatusSerializer(status_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReportView(APIView):
    def get(self, request):
        crawled_urls = CrawledURL.objects.values_list('url', flat=True).distinct()
        return Response({"urls": list(crawled_urls)}, status=status.HTTP_200_OK)

class VectorSimilarityView(APIView):
    def get(self, request):
        urls = request.query_params.getlist('urls')
        if not urls:
            return Response({"error": "URLs are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        embeddings = [model.encode(scrape_page(url)[1]) for url in urls]
        cosine_sim = util.pytorch_cos_sim(embeddings, embeddings)
        return Response({"cosine_similarity": cosine_sim.tolist()}, status=status.HTTP_200_OK)
