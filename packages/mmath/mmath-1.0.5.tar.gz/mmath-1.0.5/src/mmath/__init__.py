import math
"""
Projet d'analyse: Sujet 25
Auteur-e-s: Niloofar BAKHSHY, Ibrahima BAH, Nongma SORGHO, Asadov KAMRAN
Institution: UFR de mathematique et d'informatique, Universite de Strasbourg
Le projet: Il nous est demandé d'approcher la valeur de sin(7/4) tout en certifiant nos resultats.
            Cependant, avec la formule de Taylor
            sur R combinée a la preuve de Cauchy et a l'etablissement du certificat de convergence,
            on s'est vite rendu compte que l'on peut etendre cette definition sur R et ainsi pouvoir
            cette de maniere moduler a un ordre k les N premieres decimales du sin de tout reel.
            Ci-dessous, le programme informatique traduisant les resultats de nos analyses.
"""


class Mmath:

    def __init__(self, val):
        """
        Initialisation de la fonction generique pour les calculs menant a sin(:param val)
        :param val: Valeur numerique de type float sur laquelle portera notre analyse
        """
        self.val = val % (2 * math.pi)
        self.sin = self.r(self.preuveParCauchy(10 ** -100))
        pass

    def factoriel(self, x):
        """
        Fonction de calcul du factoriel de :param x
        :param x: Entier naturel dont on veut determiner le factoriel
        :return: Le factoriel de :param x
        """
        return 1 if x <= 1 else x * self.factoriel(x - 1)

    def tronquer(self, x, precision):
        """
        Fonction tronquant :param x a 10 ** -:param precision pres
        :param x: Flottant que l'on veut tronquer
        :param precision: Precision de troncature souhaitee
        :return: :param x tronquee a 10 ** -:param precision pres
        """
        precision = 10 ** precision
        return (int(x * precision)) / precision

    def sinusTaylorien(self, angle, precision):
        """
        Fonction calculant la valeur de la definition de sin(:param angle) selont la formule de Taylor a
        l'ordre :param precision
        :param angle: flottant dont on souhaite obtenir le sin
        :param precision: l'ordre n du calcul du developpement limité menant a sin(:param angle)
        :return: sin(:param angle) selon le developpement limité de Taylor a l'ordre n=:param precision
        """
        v = 0.0
        for n in range(precision):
            v += (((-1) ** n) * ((angle ** ((2 * n) + 1)) / self.factoriel((2 * n) + 1)))
        return v

    def r(self, n):
        """
        Suite (r(n))_n
        :param n: entier naturel representant l'indice n de la suite (r(n))_n
        :return: r(:param n)
        """
        return self.sinusTaylorien(self.val, n)

    def conv(self, k):
        """
        Certificat de convergence de la suite (r(n))_n
        :param k: entier naturel representant l'ordre k du calcul du certificat de convergence conv(k)
        :return: conv(:param k)
        """
        n = 0
        ordre = 1 / (10 ** (k))
        while True:
            n += 1
            serie_approchee = (2 ** (n + 1)) / self.factoriel(n + 1)
            if (serie_approchee <= ordre):
                break
        return n

    def preuveParCauchy(self, epsilon):
        """
        Fonction prouvant la stabilite d'un developpement limité de precision 10 ** -:param epsilon
        :param epsilon: Ordre de precision souhaite du developpement limite
        :return: L'ordre du developpement limite a partir duquel :param val est stable avec une precision(ordre)
                10 ** -:param epsilon
        """
        n = 1
        while True:
            difference_de_cauchy = self.sinusTaylorien(self.val, n) - self.sinusTaylorien(self.val, n + 1)
            n += 1
            if (abs(difference_de_cauchy) < epsilon):
                break
        return n - 1
