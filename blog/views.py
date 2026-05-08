from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import BlogPost, Comment
from .forms import BlogPostForm

def blog_list(request):
    """Afficher tous les articles publiés"""
    posts = BlogPost.objects.filter(status='published').order_by('-published_at')
    featured_posts = posts.filter(is_featured=True)[:3]
    
    all_tags = []
    for post in posts:
        if post.tags:
            all_tags.extend([tag.strip() for tag in post.tags.split(',')])
    popular_tags = list(set(all_tags))[:10]
    
    context = {
        'posts': posts,
        'featured_posts': featured_posts,
        'popular_tags': popular_tags,
    }
    return render(request, 'blog/blog.html', context)

def blog_detail(request, slug):
    """Afficher un article en détail"""
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    
    post.views += 1
    post.save()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email', '')
        comment_text = request.POST.get('comment')
        
        if name and comment_text:
            Comment.objects.create(
                post=post,
                name=name,
                email=email,
                comment=comment_text
            )
            messages.success(request, "Votre commentaire a été ajouté !")
            return redirect('blog_detail', slug=post.slug)
        else:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
    
    similar_posts = []
    if post.tags:
        post_tags = [tag.strip() for tag in post.tags.split(',')]
        similar_posts = BlogPost.objects.filter(
            status='published',
            tags__icontains=post_tags[0]
        ).exclude(id=post.id)[:3]
    
    comments = post.comments.filter(is_approved=True)
    
    context = {
        'post': post,
        'comments': comments,
        'similar_posts': similar_posts,
    }
    return render(request, 'blog/detail.html', context)

@staff_member_required
def add_blog(request):
    """Ajouter un article de blog - formulaire personnalisé"""
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # Si l'article est publié, définir la date de publication
            if post.status == 'published' and not post.published_at:
                from django.utils import timezone
                post.published_at = timezone.now()
            post.save()
            messages.success(request, f'✅ Article "{post.title}" ajouté avec succès !')
            return redirect('blog')
        else:
            messages.error(request, '❌ Erreur dans le formulaire. Vérifiez les champs.')
    else:
        form = BlogPostForm()
    
    return render(request, 'blog/add_blog.html', {'form': form})

@staff_member_required
def delete_blog(request, slug):
    """Supprimer un article (admin uniquement)"""
    post = get_object_or_404(BlogPost, slug=slug)
    title = post.title
    post.delete()
    messages.success(request, f'✅ Article "{title}" supprimé avec succès !')
    return redirect('blog')
