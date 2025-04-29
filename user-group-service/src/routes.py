from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Group, GroupMember, SecretQuestion

groups = Blueprint('groups', __name__)

@groups.route('/groups', methods=['POST'])
@jwt_required()
def create_group():
    current_user = get_jwt_identity()
    data = request.get_json()
    
    new_group = Group(
        name=data['name'],
        description=data.get('description', ''),
        admin_id=current_user
    )
    db.session.add(new_group)
    db.session.flush()
    
    # Agregar al creador como miembro administrador
    admin_member = GroupMember(
        user_id=current_user,
        group_id=new_group.id,
        role='admin',
        status='active'
    )
    db.session.add(admin_member)
    
    # Agregar preguntas secretas si se proporcionan
    if 'secret_questions' in data:
        for q in data['secret_questions']:
            question = SecretQuestion(
                group_id=new_group.id,
                question=q['question'],
                answer=q['answer'],
                created_by=current_user
            )
            db.session.add(question)
    
    db.session.commit()
    return jsonify({'message': 'Group created successfully', 'group_id': new_group.id}), 201

@groups.route('/groups/<int:group_id>/join', methods=['POST'])
@jwt_required()
def join_group(group_id):
    current_user = get_jwt_identity()
    data = request.get_json()
    
    # Verificar si el grupo existe
    group = Group.query.get_or_404(group_id)
    
    # Verificar si el usuario ya es miembro
    existing_member = GroupMember.query.filter_by(
        user_id=current_user,
        group_id=group_id
    ).first()
    
    if existing_member:
        return jsonify({'message': 'User is already a member'}), 400
    
    # Verificar respuestas a preguntas secretas
    questions = SecretQuestion.query.filter_by(group_id=group_id).all()
    user_answers = data.get('answers', [])
    
    if len(questions) != len(user_answers):
        return jsonify({'message': 'Must answer all secret questions'}), 400
    
    for q, a in zip(questions, user_answers):
        if q.answer.lower() != a.lower():
            return jsonify({'message': 'Incorrect answers'}), 403
    
    # Crear nueva membresía
    new_member = GroupMember(
        user_id=current_user,
        group_id=group_id,
        status='active'
    )
    db.session.add(new_member)
    db.session.commit()
    
    return jsonify({'message': 'Successfully joined group'}), 200

@groups.route('/groups/<int:group_id>/members', methods=['GET'])
@jwt_required()
def get_group_members(group_id):
    # Verificar si el usuario es miembro del grupo
    current_user = get_jwt_identity()
    member = GroupMember.query.filter_by(
        user_id=current_user,
        group_id=group_id,
        status='active'
    ).first()
    
    if not member:
        return jsonify({'message': 'Access denied'}), 403
    
    members = GroupMember.query.filter_by(group_id=group_id).all()
    members_list = [{
        'user_id': m.user_id,
        'role': m.role,
        'join_date': m.join_date.isoformat(),
        'status': m.status
    } for m in members]
    
    return jsonify(members_list), 200

@groups.route('/groups/my', methods=['GET'])
@jwt_required()
def get_my_groups():
    current_user = get_jwt_identity()
    memberships = GroupMember.query.filter_by(
        user_id=current_user,
        status='active'
    ).all()
    
    groups_list = []
    for membership in memberships:
        group = Group.query.get(membership.group_id)
        groups_list.append({
            'id': group.id,
            'name': group.name,
            'description': group.description,
            'role': membership.role,
            'member_count': GroupMember.query.filter_by(
                group_id=group.id,
                status='active'
            ).count()
        })
    
    return jsonify(groups_list), 200