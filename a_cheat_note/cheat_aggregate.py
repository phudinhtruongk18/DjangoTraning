
# Total number of books.
Book.objects.count()
=> 2452

# Total number of books with publisher=BaloneyPress
Book.objects.filter(publisher__name='BaloneyPress').count()
=> 73

# Average price across all books.
from django.db.models import Avg, Max, Min
Book.objects.all().aggregate(Avg('price'))
=> {'price__avg': 34.35}

#  sinh ra nhiều hơn một aggregate
Book.objects.aggregate(Avg('price'), Max('price'), Min('price'))
=> {'price__avg': 34.35, 'price__max': Decimal('81.20'), 'price__min': Decimal('12.99')}


# Max price across all books.
from django.db.models import Max
Book.objects.all().aggregate(Max('price'))
=> {'price__max': Decimal('81.20')}

# Cost per page
from django.db.models import F, FloatField, Sum
Book.objects.all().aggregate(
    price_per_page=Sum(F('price')/F('pages'), output_field=FloatField()))
=> {'price_per_page': 0.4470664529184653}

# All the following queries involve traversing the Book<->Publisher
# foreign key relationship backwards.

# Each publisher, each with a count of books as a "num_books" attribute.
from django.db.models import Count
pubs = Publisher.objects.annotate(num_books=Count('book'))
pubs
=> <QuerySet [<Publisher: BaloneyPress>, <Publisher: SalamiPress>, ...]>
pubs[0].num_books
=> 73

# The top 5 publishers, in order by number of books.
pubs = Publisher.objects.annotate(num_books=Count('book')).order_by('-num_books')[:5]
pubs[0].num_books
=> 1323


# Group by với aggregate function

User.objects
.values('is_active')
.annotate(total=Count('id'))

User.objects
.values('is_active')
.filter(is_staff=True)
.annotate(total=Count('id'))

User.objects
.values(
    'is_active', 
    'is_staff'
)
.annotate(
    total=Count('id'),
    last_joined=Max('date_joined'),
)
.order_by('is_active', 'total')

values('is_active'): trường muốn group by.
annotate(total=Count('id')): group by theo aggregate function nào.



from django.db.models import F, Q

User.objects
.values('date_joined__year')
.annotate(
    staff_users=(
        Count('id', filter=Q(is_staff=True))
    ),
    non_staff_users=(
        Count('id', filter=Q(is_staff=False))
    ),
)

User.objects
.annotate(year_joined=F('date_joined__year'))
.values('is_active')
.annotate(total=Count('id'))
.filter(total__gt=100)

User.objects
.values('is_active')
.annotate(
    total=Count('id'),
    unique_names=Count('last_name', distinct=True),
)

User.objects
.values('user_profile__type')
.annotate(total=Count('id'))

User.objects
.annotate(memberships=Count('groups'))
.values('id', 'memberships')

# add if manytomany field
entry.authors.add(joe)

# if
.filter(pub_date__year=2006)
# if not 
.exclude(pub_date__year=2006)

# 20 look up
exact 
iexact (ILIKE)
contains
icontains
in
gt (greater than)
gte (greater than or equal)
lt (less than)
lte (less than or equal)
startswith
istartswith
endswith
iendswith
range
year,iso_year,month,day,week,week_day,iso_week_day
quarter (quy trong nam)
time, hout, minute, second
isnull
search
regex
iregex
