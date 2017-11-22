
function scrollIntoElement(id)
{
    if (navigator.userAgent.search("Firefox") > -1)
    {
        document.getElementById(id).scrollIntoView({ behavior: 'smooth' })
    }
    else
    {
        document.getElementById(id).scrollIntoView()
    }
}