from django.shortcuts import render, redirect, get_object_or_404
from .models import Petition
from django.contrib.auth.decorators import login_required


def index(request):
    petitions = Petition.objects.all().order_by('-date')
    template_data = {}
    template_data['petitions'] = petitions
    return render(request, 'petitions/index.html', {'template_data': template_data})

@login_required
def create_petition(request):
    if request.method == 'POST' and request.POST['comment']!= '':
        petition = Petition()
        petition.comment = request.POST['comment']
        petition.user = request.user
        petition.save()
        return redirect('petitions.index')
    else:
        return redirect('petitions.index')

@login_required
def upvote_petition(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    if request.user in petition.upvotes.all():
        petition.upvotes.remove(request.user) # removing the user from the relationship many to many
    else:
        petition.upvotes.add(request.user) # adding the user from the relationship many to many
    petition.save()
    return redirect('petitions.index')

@login_required
def delete_petition(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id, user=request.user)
    petition.delete()
    return redirect('petitions.index')
