from django.utils import simplejson as json
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class TestVO(db.Model):
    id = db.StringProperty()
    title = db.StringProperty(default='no title')
    author = db.UserProperty()
    content = db.BlobProperty()
    
def getTestVO(user, testId):
    """Return the stored TestVO or None."""
    if not(user):
        return None
    testVOs = TestVO.gql("WHERE author = :1 AND id = :2 ORDER BY title ASC LIMIT 100", user, testId)
    for testVO in testVOs:      # un peu boeuf, peut mieux faire !
        return testVO

class MyHandler(webapp.RequestHandler):
    def get(self):
        #
        # we want the user to be authenticated
        #
        user = users.get_current_user()
        if not(user):
            #self.response.out.write("<html><body>Authentifiez vous d'abord</body></html>");
            result = ["AUTHENTICATE", users.create_login_url("/app/index.html")]
            self.response.out.write(json.dumps(result))
            return
        
        action = self.request.get('action')
        testId = self.request.get('testId')
        #
        # GET LIST
        #
        if action == "getUserTests":
            testVOs = TestVO.gql("WHERE author = :1 ORDER BY title ASC LIMIT 100", user)
            result = [];
            for testVO in testVOs:
                result.append([testVO.id, testVO.title])
            self.response.out.write(json.dumps(result));
        #
        # SAVE
        #
        if action == "saveTest":
            testVO = getTestVO(user, testId)
            if not(testVO):
                testVO = TestVO()
                testVO.id = testId
                testVO.author = user
            testVO.content = self.request.get('testDTO').encode('utf-8')
            testVO.title = self.request.get('title')
            testVO.save()   # create or update
            self.response.out.write(json.dumps(testId))
        #
        # GET
        #
        if (action == "getTest"):
            testVO = getTestVO(user, testId)
            if testVO:
                self.response.out.write(testVO.content);
        #
        # DELETE
        #
        if action == "deleteTest":
            testVO = getTestVO(user, testId)
            if testVO:
                testVO.delete();
                self.response.out.write(json.dumps("ok"))
        #
        # INIT
        #
        if action == "init":
            result = [user.nickname(), users.create_logout_url("/app/index.html")]    
            self.response.out.write(json.dumps(result))
            
        if action == "aloha":
            tests = json.loads(aloha)
            for test in tests:
                testId = test['id']
                testVO = getTestVO(user, testId)
                if not(testVO):
                    testVO = TestVO()
                    testVO.id = testId
                    testVO.author = user
                testVO.content = str(json.dumps(test))
                testVO.title = test['title']
                testVO.save()   # create or update
            
        if action == "aglae":
            tests = json.loads(aglae)
            for test in tests:
                testId = test['id']
                testVO = getTestVO(user, testId)
                if not(testVO):
                    testVO = TestVO()
                    testVO.id = testId
                    testVO.author = user
                testVO.content = str(json.dumps(test))
                testVO.title = test['title']
                testVO.save()   # create or update
                
            
    def post(self):
        self.get();

application = webapp.WSGIApplication([('/.*', MyHandler)], debug=True)

aloha="""[{"title":"Latin vocab. 24\/10 F=>L","id":"1350834554033","testItemVOs":[{"question":"\u00eatre","response":"sum es esse fui","type":""},{"question":"pouvoir","response":"possum potes posse potui","type":""},{"question":"honorer","response":"colo is ere colui cultum","type":""},{"question":"voir","response":"video es ere vidi visum","type":""},{"question":"aller","response":"eo is ire ivi itum","type":""},{"question":"sortir","response":"exeo is ire ivi itum","type":""},{"question":"prendre","response":"capio is ere cepi captum","type":""},{"question":"aimer ","response":"amo as are avi atum","type":""},{"question":"donner","response":"do as are dedi datum","type":""},{"question":"appeler","response":"voco as are avi atum","type":""},{"question":"craindre","response":"timeo es ere timui","type":""},{"question":"avoir (poss\u00e9der)","response":"habeo es ere habui habitum","type":""},{"question":"conduire","response":"duco is ere duxi ductum","type":""},{"question":"entendre","response":"audio is ire ivi itum","type":""},{"question":"envoyer","response":"mitto is ere misi missum","type":""}]},{"title":"Anglais - verbes irreguliers","id":"1350834567906","testItemVOs":[{"question":"acheter","response":"buy bought bought","type":""},{"question":"apporter","response":"bring brought brought","type":""},{"question":"couper","response":"cut cut cut","type":""}]},{"title":"Latin, vocabulaire pour le 5\/12\/12","id":"1353513933486","testItemVOs":[{"question":"la mort","response":"mors mortis f","type":""},{"question":"le compagnon, la compagne","response":"comes comitis m f","type":""},{"question":"le destin","response":"fatum i n","type":""},{"question":"la maladie","response":"morbus i m","type":""},{"question":"l'h\u00f4te","response":"hospes hospitis m","type":""},{"question":"vivre","response":"vivo is ere vixi victum","type":""},{"question":"traverser","response":"transeo is ire ivi itum","type":""},{"question":"maintenant","response":"num nunc","type":""},{"question":"toujours","response":"semper","type":""},{"question":"bien","response":"bene","type":""}]},{"title":"","id":"1354638019966","testItemVOs":[{"question":"semper","response":"toujours","type":""},{"question":"mors mortis f","response":"la mort","type":""},{"question":"morbus i m","response":"la maladie","type":""},{"question":"comes comitis m f ","response":"le compagnon la compagne","type":""},{"question":"num nunc","response":"maintenant","type":""},{"question":"bene","response":"bien","type":""},{"question":"fatum i n","response":"le destin","type":""}]},{"title":"Latin, vocabulaire pour le 5\/12\/12 L=>F","id":"1354638107463","testItemVOs":[{"question":"fatum i n","response":"le destin","type":""},{"question":"mors mortis f","response":"la mort","type":""},{"question":"morbus i m","response":"la maladie","type":""},{"question":"comes comitis m f ","response":"le compagnon la compagne","type":""},{"question":"hospes hospitis m","response":"l'h\u00f4te","type":""},{"question":"num nunc","response":"maintenant","type":""},{"question":"semper","response":"toujours","type":""},{"question":"bene","response":"bien","type":""},{"question":"vivo is ere vixi victum","response":"vivre","type":""},{"question":"transeo is ire ivi itum","response":"traverser","type":""}]},{"title":"Anglais-verbes irr\u00e9guliers (B)","id":"1355062666310","testItemVOs":[{"question":"\u00eatre","response":"be was were been","type":""},{"question":"porter supporter (n\u00e9)","response":"bear bore born borne","type":""},{"question":"battre","response":"beat beat beaten","type":""},{"question":"devenir","response":"become became become","type":""},{"question":"commencer","response":"begin began begun","type":""},{"question":"mordre","response":"bite bit bitten","type":""},{"question":"saigner","response":"bleed bled bled","type":""},{"question":"souffler","response":"blow blew blown","type":""},{"question":"casser","response":"break broke broken","type":""},{"question":"apporter","response":"bring brought brought","type":""},{"question":"diffuser \u00e9mettre","response":"broadcast broadcast broadcast","type":""},{"question":"construire","response":"build built built","type":""},{"question":"br\u00fbler","response":"burn burnt burnt ","type":""},{"question":"acheter","response":"buy bought bought","type":""}]},{"title":"Anglais-verbes irr\u00e9guliers (B) A=>F","id":"1355063479448","testItemVOs":[{"question":"be ","response":"be was were been \u00eatre","type":""},{"question":"bear","response":"bear bore born borne porter supporter","type":""},{"question":"beat","response":"beat beat beaten battre","type":""},{"question":"become ","response":"become became become devenir","type":""},{"question":"begin","response":"begin began begun commencer","type":""},{"question":"bite","response":"bite bit bitten mordre","type":""},{"question":"bleed","response":"bleed bled bled saigner","type":""},{"question":"blow","response":"blow blew blown souffler","type":""},{"question":"break","response":"break broke broken casser","type":""},{"question":"bring","response":"bring brought brought apporter","type":""},{"question":"broadcast","response":"broadcast broadcast broadcast diffuser \u00e9mettre","type":""},{"question":"build","response":"build built built construire","type":""},{"question":"burn","response":"burn burnt burnt br\u00fbler","type":""},{"question":"buy","response":"buy bought bought acheter","type":""}]},{"title":"Anglais-verbes irr\u00e9guliers (C\/D)","id":"1355649013797","testItemVOs":[{"question":"catch ","response":"catch caught caught attraper","type":""},{"question":"attraper","response":"catch caught caught","type":""},{"question":"choose ","response":"choose chose chosen choisir","type":""},{"question":"choisir","response":"choose chose chosen","type":""},{"question":"come","response":"come came come venir","type":""},{"question":"venir","response":"come came come","type":""},{"question":"cost","response":"cost cost cost co\u00fbter","type":""},{"question":"co\u00fbter","response":"cost cost cost","type":""},{"question":"cut","response":"cut cut cut couper","type":""},{"question":"couper","response":"cut cut cut","type":""},{"question":"do","response":"do did done faire","type":""},{"question":"faire","response":"do did done","type":""},{"question":"draw ","response":"draw drew drawn dessiner","type":""},{"question":"dessiner","response":"draw drew drawn","type":""},{"question":"dream","response":"dream dreamt dreamt r\u00eaver","type":""},{"question":"r\u00eaver","response":"dream dreamt dreamt","type":""},{"question":"drink","response":"drink drank drunk boire","type":""},{"question":"boire","response":"drink drank drunk","type":""},{"question":"drive ","response":"drive drove driven conduire","type":""},{"question":"conduire","response":"drive drove driven","type":""}]},{"title":"Anglais-verbes irr\u00e9guliers (E\/F)","id":"1355649994962","testItemVOs":[{"question":"eat ","response":"eat ate eaten manger","type":""},{"question":"manger","response":"eat ate eaten","type":""},{"question":"fall ","response":"fall fell fallen tomber","type":""},{"question":"tomber","response":"fall fell fallen","type":""},{"question":"feed ","response":"feed fed fed nourrir","type":""},{"question":"nourrir","response":"feed fed fed ","type":""},{"question":"feel ","response":"feel felt felt sentir ressentir","type":""},{"question":"sentir ressentir","response":"feel felt felt","type":""},{"question":"fight","response":"fight fought fought combattre se battre","type":""},{"question":"combattre se battre","response":"fight fought fought","type":""},{"question":"find","response":"find found found trouver","type":""},{"question":"trouver","response":"find found found","type":""},{"question":"fly ","response":"fly flew flown voler","type":""},{"question":"voler","response":"fly flew flown ","type":""},{"question":"forbid","response":"forbid forbade forbidden interdire","type":""},{"question":"interdire","response":"forbid forbade forbidden","type":""},{"question":"forget","response":"forget forgot forgotten oublier","type":""},{"question":"oublier","response":"forget forgot forgotten","type":""},{"question":"forgive ","response":"forgive forgave forgiven pardonner","type":""},{"question":"pardonner","response":"forgive forgave forgiven","type":""},{"question":"freeze","response":"freeze froze frozen geler","type":""},{"question":"geler","response":"freeze froze frozen","type":""}]},{"title":"Anglais-verbes irr\u00e9guliers (G\/H)","id":"1355853033436","testItemVOs":[{"question":"get","response":"get got got obtenir devenir","type":""},{"question":"obtenir","response":"get got got","type":""},{"question":"give","response":"give gave given donner","type":""},{"question":"donner","response":"give gave given","type":""},{"question":"go","response":"go went gone aller","type":""},{"question":"aller","response":"go went gone","type":""},{"question":"grow","response":"grow grew grown grandir faire pousser","type":""},{"question":"grandir faire pousser","response":"grow grew grown","type":""},{"question":"hang","response":"hang hung hung accrocher","type":""},{"question":"accrocher","response":"hang hung hung","type":""},{"question":"have ","response":"have had had avoir","type":""},{"question":"avoir ","response":"have had had","type":""},{"question":"hear","response":"hear heard heard entendre","type":""},{"question":"entendre","response":"hear heard heard","type":""},{"question":"hide","response":"hide hid hidden se cacher","type":""},{"question":"hit","response":"hit hit hit frapper","type":""},{"question":"hold","response":"hold held held tenir","type":""},{"question":"frapper ","response":"hit hit hit","type":""},{"question":"tenir","response":"hold held held","type":""},{"question":"hurt","response":"hurt hurt hurt faire mal blesser","type":""},{"question":"faire mal blesser","response":"hurt hurt hurt","type":""}]}]"""
aglae="""[{"title":"Anglais","id":"1350835092409","testItemVOs":[{"question":"maison","response":"home","type":""},{"question":"voiture","response":"car","type":""},{"question":"moi m\u00eame","response":"myself","type":""},{"question":"un enfant","response":"a child","type":""},{"question":"des enfants","response":"children","type":""},{"question":"ordinateur","response":"computer","type":""}]},{"title":"Latin","id":"1352830819064","testItemVOs":[{"question":"une d\u00e9esse","response":"dea, ae, f","type":""},{"question":"une lettre","response":"epistula, ae, f","type":""},{"question":"la for\u00eat","response":"silva, ae, f","type":""},{"question":"l'eau","response":"aqua, ae, f","type":""},{"question":"une jeune fille","response":"puella, ae, f","type":""},{"question":"une maison","response":"villa, ae, f","type":""},{"question":"une route","response":"via, ae, f","type":""},{"question":"une fille","response":"filia, ae, f","type":""},{"question":"la vie","response":"vita, ae, f","type":""},{"question":"un po\u00e8te","response":"poeta, ae, m","type":""}]},{"title":"Latin - Hercules","id":"1352831036764","testItemVOs":[{"question":"p\u00e8re et m\u00e8re","response":"Zeus \/ Jupiter et Alcm\u00e8ne une mortelle","type":""},{"question":"qu'a fait Hercules et \u00e0 quoi est-il condamn\u00e9","response":"tua ses 3 enfants, oracle \u00e0 Delphes, se mettre au service d'Eurysth\u00e9e","type":""},{"question":"N\u00e9m\u00e9e","response":"Lion","type":""},{"question":"Lerne","response":"Hydre, 8\/9 t\u00eates, sang empoisonn\u00e9","type":""},{"question":"biche","response":"de C\u00e9rynie qu'il poursuit une ann\u00e9e","type":""},{"question":"sanglier","response":"d'Erymanthe, effrayant","type":""},{"question":"cerb\u00e8re","response":"chien qui garde la porte des enfers","type":""},{"question":"pommes","response":"pommes d'or du jardin des Hep\u00e9rides","type":""},{"question":"\u00e9curies","response":"d'Augias, d\u00e9tourne 2 fleuves","type":""},{"question":"ceinture","response":"de la reine des Amazones","type":""},{"question":"boeufs","response":"de G\u00e9ryon qu'Hercules doit aller chercher au bout du monde","type":""},{"question":"les juments","response":"de Diom\u00e8de","type":""},{"question":"le taureau","response":"de Cr\u00eate, donn\u00e9 par Pos\u00e9idon \u00e0 Minos, le roi de Cr\u00eate","type":""}]},{"title":"Latin 2","id":"1355853352966","testItemVOs":[{"question":"video","response":"es ere voir","type":""},{"question":"audio","response":"is ire ecouter entendre","type":""},{"question":"capio","response":"is ire prendre","type":""},{"question":"mitto ","response":"is ere envoyer","type":""},{"question":"amo","response":"as are aimer","type":""},{"question":"do","response":"as are donner","type":""},{"question":"video","response":"es ere voir","type":""},{"question":"timeo","response":"es ere craindre","type":""},{"question":"colo","response":"is ere honorer cultiver","type":""},{"question":"duco","response":"is ere conduire","type":""}]},{"title":"latin 2 bis","id":"1355859535408","testItemVOs":[{"question":"aimer","response":"amo as are ","type":""},{"question":"donner","response":"do as are ","type":""},{"question":"conduire","response":"duco is ere ","type":""},{"question":"voir","response":"video es ere ","type":""},{"question":"craindre ","response":"timeo es ere ","type":""},{"question":"honorer cultiver","response":"colo is ere ","type":""},{"question":"envoyer","response":"mitto is ere ","type":""},{"question":"entendre ecouter","response":"audio is ire","type":""},{"question":"venir","response":"venio is ire ","type":""},{"question":"prendre ","response":"capio is ere","type":""}]}]"""

if __name__ == "__main__":
    run_wsgi_app(application)
    
