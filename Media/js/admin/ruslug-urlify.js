var RUSSIAN_MAP = {
    'а':'а', 'б':'б', 'в':'в', 'г':'г', 'д':'д', 'е':'е', 'ё':'ё', 'ж':'ж',
    'з':'з', 'и':'и', 'й':'й', 'к':'к', 'л':'л', 'м':'м', 'н':'н', 'о':'о',
    'п':'п', 'р':'р', 'с':'с', 'т':'т', 'у':'у', 'ф':'ф', 'х':'х', 'ц':'ц',
    'ч':'ч', 'ш':'ш', 'щ':'щ', 'ъ':'ъ', 'ы':'ы', 'ь':'ь', 'э':'э', 'ю':'ю',
    'я':'я',
    'А':'А', 'Б':'Б', 'В':'В', 'Г':'Г', 'Д':'Д', 'Е':'Е', 'Ё':'Ё', 'Ж':'Ж',
    'З':'З', 'И':'И', 'Й':'Й', 'К':'К', 'Л':'Л', 'М':'М', 'Н':'Н', 'О':'О',
    'П':'П', 'Р':'Р', 'С':'С', 'Т':'Т', 'У':'У', 'Ф':'Ф', 'Х':'Х', 'Ц':'Ц',
    'Ч':'Ч', 'Ш':'Ш', 'Щ':'Щ', 'Ъ':'Ъ', 'Ы':'Ы', 'Ь':'Ь', 'Э':'Э', 'Ю':'Ю',
    'Я':'Я'
}
var UKRAINIAN_MAP = {
    'Є':'Є', 'І':'І', 'Ї':'Ї', 'Ґ':'', 'є':'є', 'і':'і', 'ї':'ї', 'ґ':''
}

var ALL_DOWNCODE_MAPS=new Array()
ALL_DOWNCODE_MAPS[0]=RUSSIAN_MAP
ALL_DOWNCODE_MAPS[1]=UKRAINIAN_MAP

var Downcoder = new Object();
Downcoder.Initialize = function()
{
    if (Downcoder.map) // already made
        return ;
    Downcoder.map ={}
    Downcoder.chars = '' ;
    for(var i in ALL_DOWNCODE_MAPS)
    {
        var lookup = ALL_DOWNCODE_MAPS[i]
        for (var c in lookup)
        {
            Downcoder.map[c] = lookup[c] ;
            Downcoder.chars += c ;
        }
     }
    Downcoder.regex = new RegExp('[' + Downcoder.chars + ']|[^' + Downcoder.chars + ']+','g') ;
}

downcode= function( slug )
{
    Downcoder.Initialize() ;
    var downcoded =""
    var pieces = slug.match(Downcoder.regex);
    if(pieces)
    {
        for (var i = 0 ; i < pieces.length ; i++)
        {
            if (pieces[i].length == 1)
            {
                var mapped = Downcoder.map[pieces[i]] ;
                if (mapped != null)
                {
                    downcoded+=mapped;
                    continue ;
                }
            }
            downcoded+=pieces[i];
        }
    }
    else
    {
        downcoded = slug;
    }
    return downcoded;
}

function URLify(s, num_chars) {
    // changes, e.g., "Petty theft" to "petty_theft"
    // remove all these words from the string before urlifying
    s = downcode(s);
    removelist = ["a", "an", "as", "at", "before", "but", "by", "for", "from",
                  "is", "in", "into", "like", "of", "off", "on", "onto", "per",
                  "since", "than", "the", "this", "that", "to", "up", "via",
                  "with"];
    r = new RegExp('\\b(' + removelist.join('|') + ')\\b', 'gi');
    s = s.replace(r, '');
    // if downcode doesn't hit, the char will be stripped here
    s = s.replace(/[^-\w\s]/g, '');  // remove unneeded chars
    s = s.replace(/^\s+|\s+$/g, ''); // trim leading/trailing spaces
    s = s.replace(/[-\s]+/g, '-');   // convert spaces to hyphens
    s = s.toLowerCase();             // convert to lowercase
    return s.substring(0, num_chars);// trim to first num_chars chars
}
