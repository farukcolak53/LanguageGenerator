from os.path import join
from jpype import JClass, getDefaultJVMPath, java, shutdownJVM, startJVM


class Zemberek:

    ZEMBEREK_PATH: str = join('zemberek-full.jar')

    startJVM(
        getDefaultJVMPath(),
        '-ea',
        f'-Djava.class.path={ZEMBEREK_PATH}',
        convertStrings=False
    )

    TurkishMorphology: JClass = JClass('zemberek.morphology.TurkishMorphology')
    morphology: TurkishMorphology = TurkishMorphology.createWithDefaults()
