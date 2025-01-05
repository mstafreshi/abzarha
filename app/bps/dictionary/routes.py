from . import bp
from app.models import DictLang, Word
from flask import render_template, flash, url_for, redirect, request, current_app, g
import sqlalchemy as sa
from app import db
from .forms import LangForm, WordForm
from flask_babel import _
from flask_login import login_required

@bp.before_request
@login_required
def before_request():
    g.page = int(request.args.get('page', 1))

@bp.route('/langs', methods=['GET', 'POST'])
def langs():
    form = LangForm()
    if form.validate_on_submit():
        print('salam')
        dict_lang = DictLang(name=form.name.data.lower())
        db.session.add(dict_lang)
        db.session.commit()

        flash(_('Language added successfully.'))
        return redirect(url_for('.langs'))

    langs = db.session.scalars(sa.select(DictLang).order_by(DictLang.id.desc()))
    return render_template('langs.html', langs=langs, form=form)

@bp.route('/edit_lang/<int:id>', methods=['GET', 'POST'])
def edit_lang(id):
    lang = db.get_or_404(DictLang, id)
    form = LangForm(lang)
    if form.validate_on_submit():
        lang.name = form.name.data
        db.session.commit()
        flash(_('Language editted successfully.'))
        return redirect(url_for('.edit_lang', id=id))
    elif request.method == 'GET':
        form.name.data = lang.name

    return render_template('edit_lang.html', form=form, lang=lang, title=_('Edit language'))

@bp.route('/words/<int:lang>', methods=['GET', 'POST'])
def words(lang):
    language = db.get_or_404(DictLang, lang)

    form = WordForm()
    if form.validate_on_submit():
        word = Word()
        word.word = form.word.data
        word.pronunciation = form.pronunciation.data
        word.meaning = form.meaning.data
        word.lang = language
        db.session.add(word)
        db.session.commit()

        flash(_('Word added successfully'), category='success')
        return redirect(url_for('.words', lang=lang))

    paginated = db.paginate(sa.select(Word).where(Word.lang_id == lang).order_by(Word.id.desc()),
        per_page=current_app.config['PER_PAGE'],
        page=g.page,
        error_out=False,
    )
    return render_template('words.html', form=form, lang=language, paginated=paginated)

@bp.route('edit_word/<int:id>', methods=['GET', 'POST'])
def edit_word(id):
    word = db.get_or_404(Word, id)
    form = WordForm(model=word)
    if form.validate_on_submit():
        word.word = form.word.data
        word.meaning = form.meaning.data
        word.pronunciation = form.pronunciation.data
        db.session.commit()

        flash(_('Word ediited successfully'), category='success')
        return redirect(url_for('.edit_word', id=id, page=g.page))
    elif request.method == 'GET':
        """ TODO: must be changed """
        form.word.data = word.word
        form.meaning.data = word.meaning
        form.pronunciation.data = word.pronunciation

    return render_template('edit_word.html', form=form, word=word)

@bp.route('/flash_card/<int:lang>')
def flash_card(lang):
    language = db.get_or_404(DictLang, lang)
    paginated = db.paginate(language.words.select().order_by(Word.id.desc()), page=g.page, per_page=1)
    return render_template('flash_card.html', paginated=paginated, title=_('Flash card'))
