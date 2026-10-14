from rest_framework import serializers

from blog.models import Post, Category, Tag, Comment

# Serializer = model obyekti ⇄ JSON tərcüməçisi.
#   obyekt → dict  (GET):   PostSerializer(post).data
#   JSON → obyekt  (POST):  PostSerializer(data=request.data) → is_valid() → save()
# Dərs 11-dəki ModelForm ilə eyni fikirdir: sahələri modeldən özü götürür, yoxlayır, bazaya yazır.
#
# Nişanlar:  [DƏRS 14] müəllim · [DƏRS 14] praktikadan sonra müəllim · [PRAKTİKA 14] tələbə · [EV 14] tapşırıq 1–3 / bonus · [REFERANS 14] tələbəyə verilmir


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source="author.username")  # author_name = comment.author.username
    
    class Meta:
        model = Comment
        fields = ["id", "post", "author", "author_name", "text", "created_at"]
        read_only_fields = ["created_at"]


# [DƏRS 14] müəllim yazır
class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source="author.username")  # author_name = post.author.username
    like_count = serializers.SerializerMethodField()  # like_count = post.likes.count()
    comments = CommentSerializer(many=True, read_only=True)  # post.comments.all() → CommentSerializer → list[dict]
    
    class Meta:
        model = Post  # hansı model (ModelForm-dakı kimi)
        fields = [  # JSON-da hansı sahələr olsun
            "id",
            "title",
            "author",
            "author_name",
            "category",
            "tags",
            "content",
            "image",
            "is_published",
            "views",
            "like_count",
            "comments",
            "created_at",
        ]
        read_only_fields = [
            "views",
            "created_at",
        ]  # yalnız oxunur — POST-da göndərilsə də, nəzərə alınmır
        
    def get_like_count(self, obj):
        return obj.likes.count()  # SerializerMethodField() üçün metod. like_count = post.likes.count()


# [PRAKTİKA 14] — PostSerializer-in əkizi
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]


# [EV 14] tapşırıq 1 — CategorySerializer-in əkizi
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]
