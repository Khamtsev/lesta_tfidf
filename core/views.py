from django.shortcuts import render
from .constants import DISPLAYED_WORDS
from .forms import UploadFileForm
from .utils import calculate_tf_idf


def main(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            doc = request.FILES['file']
            results = calculate_tf_idf(doc)
            sorted_results = sorted(
                results, key=lambda x: x[2], reverse=True)[:DISPLAYED_WORDS]

            return render(
                request,
                'main.html',
                {'form': form, 'results': sorted_results}
            )
    else:
        form = UploadFileForm()

    return render(request, 'main.html', {'form': form})
